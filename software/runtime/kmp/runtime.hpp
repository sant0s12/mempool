// Copyright 2024 ETH Zurich and University of Bologna.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

#pragma once

#include "kmp/barrier.hpp"
#include "kmp/thread.hpp"
#include "kmp/types.h"

// NOLINTNEXTLINE(bugprone-reserved-identifier)
extern void __assert_func(const char *file, int line, const char *func,
                          const char *failedexpr);

namespace kmp {

namespace runtime {

extern std::array<Thread, NUM_CORES> threads __attribute__((section(".l1")));

extern Team defaultTeam __attribute__((section(".l1")));

extern std::optional<kmp_int32> requestedNumTeams;
extern std::optional<kmp_int32> requestedThreadLimit;

extern Barrier teamsBarrier __attribute__((section(".l1")));

static inline void runThread(kmp_int32 core_id) {
  threads[static_cast<kmp_uint32>(core_id)].run();
};

static inline Thread &getThread(kmp_int32 gtid) {
  return threads[static_cast<kmp_uint32>(gtid)];
};

static inline Thread &getCurrentThread() {
  return threads[mempool_get_core_id()];
};

} // namespace runtime

} // namespace kmp
