#dExchange Trading Pair Mapper

Given an list of ERC-20 tokens, will contact the dExchange factory method to find the contract address for their Exchange contract.

Uses combinatorics to find every possible pair without repeats. If no exchange exists, blank address is not added to output

#Output

Outputs to a JSON of trading pair by location. 
