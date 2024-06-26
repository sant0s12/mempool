// Copyright 2022 ETH Zurich and University of Bologna.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

#include <stdint.h>
#include <string.h>

#include "encoding.h"
#include "omp.h"
#include "printf.h"
#include "runtime.h"
#include "synchronization.h"

uint32_t *checkfirst;
uint32_t result;

void work1() {
  int sum = 0;
  for (int i = 0; i < 100; i++) {
    sum++;
  }
}

void parallel_single_manual() {
  uint32_t core_id = mempool_get_core_id();
  uint32_t num_cores = mempool_get_core_count();

  work1();

  mempool_timer_t cycles = mempool_get_timer();
  mempool_start_benchmark();

  if (!__atomic_fetch_or(checkfirst, 1, __ATOMIC_SEQ_CST)) {
    result = 100;
  }

  mempool_barrier(num_cores);
  *checkfirst = 0;

  mempool_stop_benchmark();
  cycles = mempool_get_timer() - cycles;

  if (core_id == 0) {
    printf("Manual Single Result: %d\n", result);
    printf("Manual Single Duration: %d\n", cycles);
  }
}

void omp_parallel_single() {
#pragma omp parallel
  {
    work1();

    mempool_timer_t cycles = mempool_get_timer();
    mempool_start_benchmark();

#pragma omp single
    { result = 100; }

    mempool_stop_benchmark();
    cycles = mempool_get_timer() - cycles;

#pragma omp master
    {
      printf("OMP Single Result: %d\n", result);
      printf("OMP Single Duration: %d\n", cycles);
    }
  }
}

int main() {
  uint32_t core_id = mempool_get_core_id();

#pragma omp parallel
  {
    // #ifdef VERBOSE
    if (core_id == 0) {
      printf("Initialize\n");
      *checkfirst = 0;
      result = 0;
    }

#pragma omp barrier

    parallel_single_manual();

#pragma omp barrier

    result = 0;
  }

  /*  OPENMP IMPLEMENTATION  */

  omp_parallel_single();

  return 0;
}
