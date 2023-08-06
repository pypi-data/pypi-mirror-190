from locdataMAC.logger import logger
from ensure import ensure_annotations


@ensure_annotations
def subu(a: int) -> int:
    logger.info(f"values is {a}")
    return 4 * a