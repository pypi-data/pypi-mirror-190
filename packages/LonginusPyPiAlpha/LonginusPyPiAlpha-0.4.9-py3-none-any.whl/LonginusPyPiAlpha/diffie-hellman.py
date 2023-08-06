from diffiehellman import DiffieHellman

# automatically generate two key pairs
dh1 = DiffieHellman(group=14, key_bits=2048)
dh2 = DiffieHellman(group=14, key_bits=2048)

# get both public keys
dh1_public = dh1.get_public_key()
dh2_public = dh2.get_public_key()

dh1_private = dh1.get_private_key()
dh2_private = dh2.get_private_key()

# generate shared key based on the other side's public key
dh1_shared = dh1.generate_shared_key(dh2_public)
dh2_shared = dh2.generate_shared_key(dh1_public)

