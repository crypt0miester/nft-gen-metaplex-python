# nft-gen-metaplex-python
the create_generative_art in metaplex cli was so slow to generate images for a project I was doing.

Thus this was born. 

10k images using 32 cores took 20 minutes

```
git clone https://github.com/crypt0miester/nft-gen-metaplex-python.git

virtualenv env

sudo apt install libjpeg-dev

pip install -r requirements.txt
```

create a traits-configuration.json from @metaplex/cli in candy-machine-nft.ts generate_art_configurations <directory>
  
copy the traits-configuration.json to nft-gen-metaplex-python folder

make sure the traits-configuration-file order of "breakdown" is the same as the "order"
  
change the values in traits-default.json
  
you can edit the description per nft basis in the code.
 
oh! and adjust the values of TOTAL_IMAGES and pool_size in main.py to for your needs. 
  
good luck!
