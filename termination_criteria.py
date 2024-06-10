from similarity_metrics import concat_similarity


def concat_criterion(qrs_target, qrs):
    return concat_similarity(qrs_target, qrs) >= 0.975
