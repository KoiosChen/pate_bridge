import os


def start(image_name, product_name, contract_name):
    start_result = os.popen(f'docker run {image_name} {product_name} {contract_name}')
    return start_result


def validate(image_name, product_name, contract_name):
    pass
