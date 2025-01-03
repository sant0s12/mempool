# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import subprocess
import os
import re
import pandas as pd
import runner
from pprint import pp

APPS_DIR = "../apps"
OMP_APPS_DIR = APPS_DIR + "/omp"
UART_REGEX = re.compile(r"\[UART\] ((?!.*\bresult\b).*): (\d+)", re.IGNORECASE)
GIT_COMMIT_HASH = subprocess.check_output(
    ["git", "describe", "--always", "--dirty"]).strip().decode("utf-8")
OUTPUT = f"results/{GIT_COMMIT_HASH}/results.csv"

results = pd.DataFrame(columns=["app", "name", "compiler", "cycles"])


def compileAll(dir, env):
    return subprocess.run(["make", "-C", dir, "all"], env=env).returncode == 0


def runAll(dir, args, env):
    global results
    compiler = env["COMPILER"]

    for app in os.listdir(dir):
        try:
            if (os.path.isfile(os.path.join(dir, app)) or app.startswith(".")):
                continue

            if not "workload" in app:
                continue

            app_dir = f"{os.path.basename(dir)}/{app}"

            (res, reason, output) = runner.run(
                app_dir, args, env, lambda x: None)
            if not res:
                print(f"{app} did not run successfully")
                print(reason)

            matches = UART_REGEX.findall(output)
            for match in matches:
                results = pd.concat([results, pd.DataFrame(
                    [{"app": app, "name":
                      match[0], "compiler":
                      compiler, "cycles":
                      int(match[1])}])])

            pp(results)
            print()
            results.to_csv(OUTPUT, index=False)

        except KeyboardInterrupt:
            continue


def main():
    parser = runner.get_arg_parser()
    args = parser.parse_args()

    env = os.environ

    env["config"] = args.config
    if not args.debug:
        env["NDEBUG"] = "1"

    os.makedirs(f'results/{GIT_COMMIT_HASH}', exist_ok=True)

    for compiler in (["gcc", "llvm"] if args.compiler is None else
                     [args.compiler]):
        env["COMPILER"] = compiler
        if compileAll(OMP_APPS_DIR, env):
            runAll(OMP_APPS_DIR, args, env)
        else:
            print(f"Failed to compile with {compiler}")


if __name__ == '__main__':
    main()
