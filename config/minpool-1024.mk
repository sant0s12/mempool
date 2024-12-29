# Copyright 2021 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

# Author: Matheus Cavalcante, ETH Zurich

###############
##  MinPool  ##
###############

include $(MEMPOOL_DIR)/config/minpool.mk

# Size of sequential memory per core (in bytes)
# (must be a power of two)
seq_mem_size ?= 1024

# Size of stack in sequential memory per core (in bytes)
stack_size ?= 1024

# Disable Xpulpimg
xpulpimg ?= 0
