import math

import numpy as np
import pytest

from simulations import integration, monty_hall, st_petersburg


class TestMontyHall:

    @pytest.mark.parametrize("strategy,expected", [("stay", 1 / 3), ("switch", 2 / 3),
                                                   ("coin", 1 / 2)])
    def test_lands_within_reach_of_the_exact_answer(self, strategy, expected):
        outcome = monty_hall.play(strategy, 200_000, seed=1)

        assert outcome.error < 0.01, outcome.format()
        assert outcome.expected == pytest.approx(expected)

    def test_switching_wins_exactly_when_staying_loses(self):
        """The two strategies partition the games; their rates must sum to one."""
        stay = monty_hall.play("stay", 50_000, seed=7)
        switch = monty_hall.play("switch", 50_000, seed=7)

        assert stay.rate + switch.rate == pytest.approx(1.0)

    def test_a_run_is_reproducible(self):
        assert monty_hall.play("switch", 1000, seed=3).wins == \
               monty_hall.play("switch", 1000, seed=3).wins

    def test_rejects_a_strategy_it_does_not_know(self):
        with pytest.raises(ValueError):
            monty_hall.play("peek", 10)


class TestIntegration:

    def test_the_integrand_traces_a_quarter_circle(self):
        x = np.linspace(0, 1, 5)
        assert integration.integrand(x)[0] == pytest.approx(1.0)
        assert integration.integrand(x)[-1] == pytest.approx(0.0)

    def test_the_estimate_closes_on_the_true_value(self):
        rough = integration.estimate(100, seed=2)
        fine = integration.estimate(200_000, seed=2)

        assert fine.error < rough.error
        assert fine.error < 0.005

    def test_the_reported_standard_error_predicts_the_real_one(self):
        """The run's own variance should say how far off it is likely to be."""
        estimate = integration.estimate(100_000, seed=4)

        assert estimate.error < 3 * estimate.standard_error

    def test_variance_settles_while_the_error_shrinks(self):
        """Variance describes the integrand, not the estimate, so it does not fall."""
        small = integration.estimate(10_000, seed=5)
        large = integration.estimate(500_000, seed=5)

        assert large.variance == pytest.approx(small.variance, abs=0.01)
        assert large.error < small.error


class TestStPetersburg:

    def test_every_payout_is_a_power_of_two(self):
        values = st_petersburg.payouts(5_000, seed=6)

        assert (values >= 1).all()
        assert np.allclose(np.log2(values), np.round(np.log2(values)))

    def test_half_the_games_pay_the_minimum(self):
        """A tail on the first toss ends the game, and that happens half the time."""
        values = st_petersburg.payouts(200_000, seed=8)

        assert (values == 1).mean() == pytest.approx(0.5, abs=0.01)

    def test_a_single_long_run_can_average_less_than_a_short_one(self):
        """One rare huge payout moves the mean more than a million ordinary ones.

        This is the paradox itself, so it is asserted rather than worked
        around: no single run's average is evidence about the next run's.
        """
        short = st_petersburg.play(10_000, seed=9)
        long = st_petersburg.play(1_000_000, seed=10)

        assert short.mean_payout > long.mean_payout
        assert short.largest_payout < long.largest_payout

    def test_the_mean_climbs_with_run_length_once_runs_are_averaged(self):
        def average(games):
            return sum(st_petersburg.play(games, seed=s).mean_payout
                       for s in range(12)) / 12

        assert average(1_000_000) > average(10_000) > average(100)

    def test_the_prediction_follows_log_of_the_run_length(self):
        round_ = st_petersburg.play(1_048_576, seed=10)

        assert round_.predicted == pytest.approx(math.log2(1_048_576) / 2 + 1)
