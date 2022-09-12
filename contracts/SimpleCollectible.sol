// SPDX-License-Identifier: MIT
pragma solidity <0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

// ERC721 contract is the Solidity name for NFT(non fungible tokens)
// These tokens are not similar to each other, i.e, like 1 WETH = 1 WETH, 1 NFT != 1 NFT
// They are all unique and mainly used to trade for images.
// So, since all blockchains work by hashing, the images used for NFT are also hashed offchain, and then brought in-chain
// To trade for other tokens or ETH.

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    // This ERC721 is a factory contract, it can only mint the same type of NFT as this shiba-inu we have chosen.
    // So we are gonna create a function called createCollectible which will help create multiple different NFTs
    // and all of this is stored in this single contract.
    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newtokenID = tokenCounter;
        _safeMint(msg.sender, newtokenID);
        _setTokenURI(newtokenID, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newtokenID;
    }
}
