import os


def start(**kwargs):
    """
    docker run --rm -v $HOST_ROOT:$DOCKER_ROOT --name pate_$filename $IMAGE_NAME python $PATE_PYZ
    -c $DOCKER_ROOT/agent.json -sc $DOCKER_ROOT/$STRATEGY_NAME/$filename > $LOG_DIR/$filename.log 2>&1 &
    """
    docker_params = 'docker run --rm --cpuset="1-47"'
    if network_mapping:
        docker_params = " ".join([docker_params, "-p", network_mapping])

    if image_name:
        docker_params = " ".join([docker_params, "-d", image_name])

    contain_id = os.popen(docker_params)
    return contain_id


def validate(image_name, product_name, contract_name):
    pass
