// Copyright 2024 ETH Zurich and University of Bologna.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

#include <stdint.h>
#include <string.h>

#include "data.h"
#include "encoding.h"
#include "omp.h"
#include "printf.h"
#include "runtime.h"
#include "synchronization.h"

#include "baremetal/mempool_matmul_i32p.h"
#include "baremetal/mempool_matmul_i32s.h"
#include "omp/mempool_matmul_i32.h"

void spmv(int *y, int *data, int *colidx, int *rowb, int *rowe, int *x, int n) {
  int i, j;
  int sum;
  int rowstart;
  int rowend;
  for (i = 0; i < n; i++) {
    sum = 0;
    rowstart = rowb[i];
    rowend = rowe[i];
    for (j = rowstart; j < rowend; j++) {
      sum += data[j] * x[colidx[j]];
    }
    y[i] = sum;
  }
}

void spmv_static(int *y, int *data, int *colidx, int *rowb, int *rowe, int *x,
                 int n) {
  int i, j;
  int sum;
  int rowstart;
  int rowend;
#pragma omp parallel for num_threads(16)
  for (i = 0; i < n; i++) {
    sum = 0;
    rowstart = rowb[i];
    rowend = rowe[i];
    for (j = rowstart; j < rowend; j++) {
      sum += data[j] * x[colidx[j]];
    }
    y[i] = sum;
  }
}

void spmv_dynamic(int *y, int *data, int *colidx, int *rowb, int *rowe, int *x,
                  int n) {
  int i, j;
  int sum;
  int rowstart;
  int rowend;
#pragma omp parallel for num_threads(16) schedule(dynamic, 4)
  for (i = 0; i < n; i++) {
    sum = 0;
    rowstart = rowb[i];
    rowend = rowe[i];
    for (j = rowstart; j < rowend; j++) {
      sum += data[j] * x[colidx[j]];
    }
    y[i] = sum;
  }
}

// Define Matrix dimensions:
// C = AB with A=[MxN], B=[NxP], C=[MxP]
#define M 32
#define N 32
#define P 32
// Specify how the matrices A and B should be initialized
// The entries will follow this format:
// a(i,j) = A_a*i + A_b*j + A_c
// b(i,j) = B_a*i + B_b*j + B_c
// The result will be the following matrix
// c(i,j) = (A_a*B_b*i*j + A_a*B_c*i + A_c*B_b*j + A_c*B_c) * N
//        + (A_a*B_a*i + A_b*B_b*j + A_b*B_c + B_a*A_c) * (N*(N-1))/2
//        + (A_b*B_a) * (N*(N-1)*(2*N-1))/6
// Note: To keep the code simpler, we use indices that go from 0 to N-1 instead
// of 1 to N as the mathematicians do. Hence, for A, i=[0,M-1] j=[0,M-1]
#define A_a 1
#define A_b 1
#define A_c -32
#define B_a 2
#define B_b 1
#define B_c 16

int32_t a[M * N] __attribute__((section(".l1")));
int32_t b[N * P] __attribute__((section(".l1")));
int32_t c[M * P] __attribute__((section(".l1")));

// Initialize the matrices in parallel
void init_matrix(int32_t *matrix, uint32_t num_rows, uint32_t num_columns,
                 int32_t a, int32_t b, int32_t c, uint32_t core_id,
                 uint32_t num_cores) {
  // Parallelize over rows
  for (uint32_t i = core_id; i < num_rows; i += num_cores) {
    for (uint32_t j = 0; j < num_columns; ++j) {
      matrix[i * num_columns + j] = a * (int32_t)i + b * (int32_t)j + c;
    }
  }
}

int32_t dot_product_sequential(int32_t const *__restrict__ A,
                               int32_t const *__restrict__ B,
                               uint32_t num_elements) {
  uint32_t i;
  int32_t dotp = 0;
  for (i = 0; i < num_elements; i++) {
    dotp += A[i] * B[i];
  }
  return dotp;
}

int32_t dot_product_omp_static(int32_t const *__restrict__ A,
                               int32_t const *__restrict__ B,
                               uint32_t num_elements) {
  uint32_t i;
  int32_t dotp = 0;
#pragma omp parallel for reduction(+ : dotp)
  for (i = 0; i < num_elements; i++) {
    dotp += A[i] * B[i];
  }
  return dotp;
}

// Initialize the matrices in parallel
void init_vector(int32_t *vector, uint32_t num_elements, int32_t a, int32_t b,
                 uint32_t core_id, uint32_t num_cores) {
  // Parallelize over rows
  for (uint32_t i = core_id; i < num_elements; i += num_cores) {
    vector[i] = a * (int32_t)i + b;
  }
}

int main() {
  mempool_timer_t cycles;

  printf("Starting SPMV Benchmark\n");
  for (int n = 1; n <= 512; n *= 2) {
    mempool_timer_t duration = 0;

    for (int i = 0; i < 10; i++) {
      cycles = mempool_get_timer();
      mempool_start_benchmark();
      spmv(y, nnz, col, rowb, rowe, x, n);
      mempool_stop_benchmark();
      cycles = mempool_get_timer() - cycles;
      duration += cycles;
    }

    printf("Sequential SPMV Duration with size %d: %d\n", n, duration / 10);

    duration = 0;
    for (int i = 0; i < 10; i++) {
      cycles = mempool_get_timer();
      mempool_start_benchmark();
      spmv_static(y, nnz, col, rowb, rowe, x, n);
      mempool_stop_benchmark();
      cycles = mempool_get_timer() - cycles;
      duration += cycles;
    }

    printf("Static SPMV Duration with size %d: %d\n", n, duration / 10);

    duration = 0;
    for (int i = 0; i < 10; i++) {
      cycles = mempool_get_timer();
      mempool_start_benchmark();
      spmv_dynamic(y, nnz, col, rowb, rowe, x, n);
      mempool_stop_benchmark();
      cycles = mempool_get_timer() - cycles;
      duration += cycles;
    }

    printf("Dynamic SPMV Duration with size %d: %d\n", n, duration / 10);
  }

  return 0;

#pragma omp parallel
  {
    // Initialize Matrices
    init_matrix(a, M, N, A_a, A_b, A_c, omp_get_thread_num(),
                omp_get_num_threads());
    init_matrix(b, N, P, B_a, B_b, B_c, omp_get_thread_num(),
                omp_get_num_threads());
  }

  printf("Starting Matrix Multiplication Benchmark\n");
  for (unsigned int n = 1; n <= 32; n *= 2) {
    cycles = mempool_get_timer();
    mempool_start_benchmark();
    mat_mul_sequential(a, b, c, n, n, n);
    mempool_stop_benchmark();
    cycles = mempool_get_timer() - cycles;
    printf("Sequential MM Duration with size %d: %d\n", n, cycles);

    cycles = mempool_get_timer();
    mempool_start_benchmark();
    mat_mul_parallel_omp(a, b, c, n, n, n);
    mempool_stop_benchmark();
    cycles = mempool_get_timer() - cycles;
    printf("Parallel MM Duration with size %d: %d\n", n, cycles);
  }

  int res = 0;

  printf("Starting Dot Product Benchmark\n");
  for (unsigned int i = 1; i <= 4096; i *= 2) {
    int32_t *a = simple_malloc(i * sizeof(int32_t));
    int32_t *b = simple_malloc(i * sizeof(int32_t));

    cycles = mempool_get_timer();
    mempool_start_benchmark();
    res = dot_product_sequential(a, b, i);
    mempool_stop_benchmark();
    cycles = mempool_get_timer() - cycles;

    printf("Sequential Dot Product duration with %d elements: %d\n", i, cycles);

    cycles = mempool_get_timer();
    mempool_start_benchmark();
    dot_product_omp_static(a, b, i);
    mempool_stop_benchmark();
    cycles = mempool_get_timer() - cycles;

    printf("Static Dot Product duration with %d elements: %d\n", i, cycles);

    simple_free(a);
  }

  printf("res: %d\n", res);

  return 0;
}
