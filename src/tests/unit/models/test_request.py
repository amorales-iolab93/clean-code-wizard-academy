
from app.models.request import WizardGrimorieTypes, WizardRequestEntity
from collections import Counter

def test_clover_random_assignation_probability_greater_than():
    """
    Ensures that the probability of a grimorie of 4 leaf being signed is between 5 and 10 percent
    """
    request_samples = 100000
    choices_clover = [WizardRequestEntity.get_random_grimorie() for _ in range(request_samples)]
    counter = Counter(choices_clover)
    total_sample = sum(counter.values())

    prob_4_clover = counter.get(WizardGrimorieTypes.FOUR_LEAF, 0) / total_sample

    assert 0.05 <= prob_4_clover <= 0.10, "The probability of FOUR_LEAF is outside the expected range"
