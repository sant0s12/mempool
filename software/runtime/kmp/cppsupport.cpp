// Copyright 2024 ETH Zurich and University of Bologna.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

#include <cstdlib>
#include <mutex>

#include "kmp/util.hpp"

extern "C" {
#include "alloc.h"
}

extern void (*_eoc)(void);

kmp::Mutex allocLock __attribute__((section(".l1")));

void *operator new(size_t size) {
  std::lock_guard<kmp::Mutex> lock(allocLock);
  void *ptr = simple_malloc(size);
  return ptr;
}

void operator delete(void *ptr) noexcept {
  std::lock_guard<kmp::Mutex> lock(allocLock);
  return simple_free(ptr);
}

void *operator new[](size_t size) { return operator new(size); }

void operator delete[](void *ptr) noexcept { return operator delete(ptr); }

namespace std {
void __throw_bad_alloc() {
  printf("Bad alloc\n");
  abort();
}

void __throw_length_error(const char *msg) {
  printf("Length error: %s\n", msg);
  abort();
}

void __throw_bad_optional_access() {
  printf("Bad optional access\n");
  abort();
}
} // namespace std

extern "C" void abort() {
  printf("Aborting\n");
  while (true) {
    asm("j _eoc");
  }
}

extern "C" int __cxa_atexit(void (*func)(void *), void *arg, void *dso_handle) {
  (void)func;
  (void)arg;
  (void)dso_handle;
  return 0;
}

extern "C" void __assert_func(const char *file, int line, const char *func,
                              const char *failedexpr) {
  printf("Assertion failed: %s, file %s, line %d, function %s\n", failedexpr,
         file, line, func);
  abort();
}
