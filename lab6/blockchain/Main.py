import datetime
from blockchain.BlockChain import Block

# Функция, которая будет возвращать нам первый блок.
# Этот блок будет иметь номер 0 и произвольные данные с произвольным значением хэша "предыдущего блока".
def create_genesis_block():
    return Block(0, datetime.datetime.now(), "Первый блок", "0")

# Функция, которая будет создавать следующие блоки в цепочке.
# Эта функция будет принимать предыдущий блок в цепи как параметр,
# создавать данные и возвращать новый блок с корректными хэшами
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = datetime.datetime.now()
    this_data = "Это блок " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

# Создаем блокчейн и первый блок
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Количество блоков, которые добавятся после первого
num_of_blocks_to_add = 20

# Добавление блоков
for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print("Блок №{} был добавлен в цепочку блоков!".format(block_to_add.index))
    print("Hash: {}\n".format(block_to_add.hash))