#!/usr/bin/env python3
# Copyright (c) 2018 Nobody
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test perforance of descendant package (chained transactions)"""
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
        ''' our test network requires a peer node so that getblocktemplate succeeds '''
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

    def mine_blocks(self):
        ''' Mine some blocks and have them mature. '''
        self.nodes[0].generate(101)
        self.utxo = self.nodes[0].listunspent(10)
        self.txid = self.utxo[0]['txid']
        self.vout = self.utxo[0]['vout']
        self.value = self.utxo[0]['amount']
        self.fee = Decimal("0.0001")
        self.tip = int("0x" + self.nodes[0].getbestblockhash(), 0)
        self.block_time = int(time.time()) + 1

    def send_chain_to_node(self):
        ''' Generates tx chain and send it to node '''
        for i in range(CHAINED_TX):
            (sent_txid, sent_value, this_sendtx, tx_size) = self.chain_transaction(
                self.nodes[0], self.txid, 0, self.value, self.fee, 1)
            self.txid = sent_txid
            self.value = sent_value
            self.chain.append(self.txid)
            self.mempool_send += this_sendtx
            self.mempool_size += tx_size

    def create_new_block(self):
        ''' Create a new block with an anyone-can-spend coinbase '''
        block = create_block(
            self.tip, create_coinbase(self.height), self.block_time)
        self.block_time += 1
        block.solve()
        return block

    def mempool_count(self):
        ''' get count of tx in mempool '''
        mininginfo = self.nodes[0].getmininginfo()
        return mininginfo['pooledtx']

    def run_test(self):
        self.log.info('Starting Test with {0} Chained Transactions'.format(CHAINED_TX))

        self.mine_blocks()

        self.mempool_send = 0
        self.mempool_size = 0
        self.chain = []

        self.send_chain_to_node()
        # mempool should have all our tx
        assert(self.mempool_count() == CHAINED_TX)

        self.height = 1

        # create new block and save coinbase
        self.block1 = self.create_new_block()
        self.tip = self.block1.sha256
        self.height += 1

        #mature the block so we can spend the coinbase
        for i in range(100):
            block = self.create_new_block()
            self.tip = block.sha256
            self.height += 1

        #block2 = create_new_block()

        self.runs=[]
        for test_iteration in range(TEST_ITERATIONS):
            gbt_start = time.perf_counter()
            # assemble a block and validate all tx in it
            templat = self.nodes[0].getblocktemplate()
            gbt_stop = time.perf_counter()
            assert(len(templat['transactions']) == CHAINED_TX)
            self.runs.append(gbt_stop - gbt_start)

        #assert(self.mempool_count() == 0)

        self.log.info('Mempool size {0}'.format(self.mempool_size))
        self.log.info('Send Tx took {0:.5f}s'.format(self.mempool_send))
        if len(self.runs) > 1:
            self.log.info('run times {}'.format(self.runs))
        self.log.info('GetBlkT took {0:.5f}s'.format(sum(self.runs)/len(self.runs)))

if __name__ == '__main__':
    ChainedTest().main()
