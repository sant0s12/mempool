// Copyright 2024 ETH Zurich and University of Bologna.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

#include "kmp/task.hpp"
#include "kmp/runtime.hpp"

extern "C" {
#include "runtime.h"
}

namespace kmp {
Task::Task(kmpc_micro func, void **args, kmp_int32 argc)
    : func(func), argc(argc), args(args) {

  assert(argc <= MAX_ARGS && "Unsupported number of microtask arguments");

  DEBUG_PRINT("Microtask constructor\n");
};

void Task::run(kmp_int32 gtid, kmp_int32 tid) const {
  // There seems to not be a better way to do this without custom passes or
  // ASM
  switch (argc) {
  default:
    return;

  // NOLINTBEGIN(cppcoreguidelines-pro-bounds-pointer-arithmetic,*-magic-numbers)
  case 0:
    func(&gtid, &tid);
    break;
  case 1:
    func(&gtid, &tid, args[0]);
    break;
  case 2:
    func(&gtid, &tid, args[0], args[1]);
    break;
  case 3:
    func(&gtid, &tid, args[0], args[1], args[2]);
    break;
  case 4:
    func(&gtid, &tid, args[0], args[1], args[2], args[3]);
    break;
  case 5:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4]);
    break;
  case 6:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5]);
    break;
  case 7:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6]);
    break;
  case 8:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7]);
    break;
  case 9:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7], args[8]);
    break;
  case 10:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7], args[8], args[9]);
    break;
  case 11:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7], args[8], args[9], args[10]);
    break;
  case 12:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7], args[8], args[9], args[10], args[11]);
    break;
  case 13:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7], args[8], args[9], args[10], args[11], args[12]);
    break;
  case 14:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7], args[8], args[9], args[10], args[11], args[12],
         args[13]);
    break;
  case 15:
    func(&gtid, &tid, args[0], args[1], args[2], args[3], args[4], args[5],
         args[6], args[7], args[8], args[9], args[10], args[11], args[12],
         args[13], args[14]);
    break;
  }
  // NOLINTEND(cppcoreguidelines-pro-bounds-pointer-arithmetic,*-magic-numbers)
};

} // namespace kmp
