#!/usr/bin/env python3
# Copyright (c) 2018 Nobody
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test descendant package tracking code."""
import time
import copy
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import *
from test_framework.mininode import COIN
from test_framework.blocktools import *

"""Read optional arguments from command line"""
CHAINED_TX = 25
if len(sys.argv)>1:
    CHAINED_TX = int(sys.argv[1])
TEST_ITERATIONS = 1
if len(sys.argv)>2:
    TEST_ITERATIONS = int(sys.argv[2])
MAX_ANCESTORS = CHAINED_TX
MAX_DESCENDANTS = CHAINED_TX

class ChainedTest(BitcoinTestFramework):

    def set_test_params(self):
        self.num_nodes = 2
        chained_args = ["-limitancestorcount=5000", "-limitdescendantcount=5000",
                        "-limitancestorsize=1000", "-limitdescendantsize=1000"
                       ]
        self.extra_args = [chained_args, chained_args]

    # Build a transaction that spends parent_txid:vout
    # Return amount sent
    def chain_transaction(self, node, parent_txid, vout, value, fee, num_outputs):
        send_value = satoshi_round((value - fee) / num_outputs)
        inputs = [{'txid': parent_txid, 'vout': vout}]
        outputs = {}
        for i in range(num_outputs):
            outputs[node.getnewaddress()] = send_value
        rawtx = node.createrawtransaction(inputs, outputs)
        signedtx = node.signrawtransaction(rawtx)

        #measure the performance of sending the raw transaction to the node
        sendtx_start = time.perf_counter()
        txid = node.sendrawtransaction(signedtx['hex'])
        sendtx_stop = time.perf_counter()
        fulltx = node.getrawtransaction(txid, 1)

        #fulltx_hex = node.getrawtransaction(txid, 0)
        #self.log.info(fulltx_hex)
        #self.log.info(len(fulltx_hex))
        #sys.getsizeof(fulltx_hex)
        # make sure we didn't generate a change output
        assert(len(fulltx['vout']) == num_outputs)
        return (txid, send_value, sendtx_stop - sendtx_start, fulltx['size'])

    def run_test(self):
        self.log.info('Starting Test with {0} Chained Transactions'.format(CHAINED_TX))

        ''' Mine some blocks and have them mature. '''
        self.nodes[0].generate(101)
        utxo = self.nodes[0].listunspent(10)
        txid = utxo[0]['txid']
        vout = utxo[0]['vout']
        value = utxo[0]['amount']
        fee = Decimal("0.0001")

        self.tip = int("0x" + self.nodes[0].getbestblockhash(), 0)
        self.block_time = int(time.time()) + 1

        # MAX_ANCESTORS transactions off a confirmed tx should be fine
        mempool_send = 0
        mempool_size = 0
        chain = []
        for i in range(CHAINED_TX):
            (txid, sent_value, this_sendtx, tx_size) = self.chain_transaction(
                self.nodes[0], txid, 0, value, fee, 1)
            value = sent_value
            chain.append(txid)
            mempool_send += this_sendtx
            mempool_size += tx_size

        '''
        Create a new block with an anyone-can-spend coinbase
        '''
        height = 1
        block = create_block(
            self.tip, create_coinbase(height), self.block_time)
        self.block_time += 1
        block.solve()
        # Save the coinbase for later
        self.block1 = block
        self.tip = block.sha256
        height += 1

        '''
        Now we need that block to mature so we can spend the coinbase.
        '''
        for i in range(100):
            block = create_block(
                self.tip, create_coinbase(height), self.block_time)
            block.solve()
            self.tip = block.sha256
            self.block_time += 1
            height += 1

        block2 = create_block(
            self.tip, create_coinbase(height), self.block_time)
        self.block_time += 1

        #assert templat.txcount == CHAINED_TX

        runs=[]
        for test_iteration in range(TEST_ITERATIONS):
            gbt_start = time.perf_counter()
            #validate the block
            templat = self.nodes[0].getblocktemplate()
            gbt_stop = time.perf_counter()
            runs.append(gbt_stop - gbt_start)

        self.log.info('Mempool size {0}'.format(mempool_size))
        self.log.info('Send Tx took {0:.5f}s'.format(mempool_send))
        self.log.info('GetBlkT took {0:.5f}s'.format(sum(runs)/len(runs)))

if __name__ == '__main__':
    ChainedTest().main()
