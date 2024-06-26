# See LICENSE for license details.

#*****************************************************************************
# access.S
#-----------------------------------------------------------------------------
#
# Test access-exception behavior.
#

#include "riscv_test.h"
#include "test_macros.h"

RVTEST_RV64M
RVTEST_CODE_BEGIN

  .align 2

  # Flipping just the MSB should result in an illegal address for RV64.
  la t2, fail
  li t0, 1 << (__riscv_xlen - 1)
  xor t0, t0, t2

  # jalr to an illegal address should commit (hence should write rd).
  # after the pc is set to rs1, an access exception should be raised.
  li TESTNUM, 2
  li t1, CAUSE_FETCH_ACCESS
  la s1, 1f
  li t2, 0
  jalr t2, t0
1:

  # A load to an illegal address should not commit.
  li TESTNUM, 3
  li t1, CAUSE_LOAD_ACCESS
  la s1, 1f
  mv t2, s1
  lb t2, (t0)
  j fail
1:

  j pass

  TEST_PASSFAIL

  .align 2
  #ifdef LLVM
  .weak mtvec_handler
  #else
  .global mtvec_handler
  #endif
mtvec_handler:
  li a0, 2
  beq TESTNUM, a0, 2f
  li a0, 3
  beq TESTNUM, a0, 2f
  j fail

2:
  bne t2, s1, fail

  csrr t2, mcause
  bne t2, t1, fail

  csrw mepc, s1
  mret

RVTEST_CODE_END

  .data
RVTEST_DATA_BEGIN

  TEST_DATA

RVTEST_DATA_END
