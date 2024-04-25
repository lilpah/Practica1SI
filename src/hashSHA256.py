import hashlib


def hashSHA256(texto):
    hasher = hashlib.sha256()
    hasher.update(texto.encode('utf-8'))
    hash_resultado = hasher.hexdigest()
    return hash_resultado