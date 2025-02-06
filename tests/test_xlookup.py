"""Test cases for the xlookup function."""
import pytest
import numpy as np
from excel_in_python import xlookup, MatchMode, SearchMode


# Define a fixture for the numeric lookup array


@pytest.fixture
def data():
    """Fixture to provide a numeric lookup array with a text return array."""
    lookup = [133, 306, 533, 273, 657, 671, 751, 893, 956, 504, 11,
              767, 170, 27, 433, 826, 427, 209, 645, 136, 362, 582,
              862, 313, 197, 1, 715, 54, 397, 178, 209]

    # create a list called text_values from a cycler of greek letter spelled out
    text_values = [
        ["alpha", "beta", "gamma", "delta", "epsilon"],
        ["zeta", "eta", "theta", "iota", "kappa"],
        ["lambda", "mu", "nu", "xi", "omicron"],
        ["pi", "rho", "sigma", "tau", "upsilon"],
        ["phi", "chi", "psi", "omega", "alpha2"],
        ["beta2", "gamma2", "delta2", "epsilon2", "zeta2"],
        ["eta2", "theta2", "iota2", "kappa2", "lambda2"],
        ["mu2", "nu2", "xi2", "omicron2", "pi2"],
        ["rho2", "sigma2", "tau2", "upsilon2", "phi2"],
        ["chi2", "psi2", "omega2", "alpha3", "beta3"],
        ["gamma3", "delta3", "epsilon3", "zeta3", "eta3"],
        ["theta3", "iota3", "kappa3", "lambda3", "mu3"],
        ["nu3", "xi3", "omicron3", "pi3", "rho3"],
        ["sigma3", "tau3", "upsilon3", "phi3", "chi3"],
        ["psi3", "omega3", "alpha4", "beta4", "gamma4"],
        ["delta4", "epsilon4", "zeta4", "eta4", "theta4"],
        ["iota4", "kappa4", "lambda4", "mu4", "nu4"],
        ["xi4", "omicron4", "pi4", "rho4", "sigma4"],
        ["tau4", "upsilon4", "phi4", "chi4", "psi4"],
        ["omega4", "alpha5", "beta5", "gamma5", "delta5"],
        ["epsilon5", "zeta5", "eta5", "theta5", "iota5"],
        ["kappa5", "lambda5", "mu5", "nu5", "xi5"],
        ["omicron5", "pi5", "rho5", "sigma5", "tau5"],
        ["upsilon5", "phi5", "chi5", "psi5", "omega5"],
        ["alpha6", "beta6", "gamma6", "delta6", "epsilon6"],
        ["zeta6", "eta6", "theta6", "iota6", "kappa6"],
        ["lambda6", "mu6", "nu6", "xi6", "omicron6"],
        ["pi6", "rho6", "sigma6", "tau6", "upsilon6"],
        ["phi6", "chi6", "psi6", "omega6", "alpha7"],
        ["beta7", "gamma7", "delta7", "epsilon7", "zeta7"],
        ["eta7", "theta7", "iota7", "kappa7", "lambda7"]
    ]
    return list(zip(lookup, text_values))


# Parametrize test cases with combinations of inputs
@pytest.mark.parametrize(
    "lookup_value, match_mode, search_mode, expected_result, should_sort",
    [
        (209, MatchMode.EXACT, SearchMode.FROM_FIRST, [
         'xi4', 'omicron4', 'pi4', 'rho4', 'sigma4'], False),
        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_FIRST, [
         'gamma3', 'delta3', 'epsilon3', 'zeta3', 'eta3'], False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_FIRST, [
         'zeta6', 'eta6', 'theta6', 'iota6', 'kappa6'], False),
        (209, MatchMode.NEXT_LARGER, SearchMode.FROM_FIRST, [
         'xi4', 'omicron4', 'pi4', 'rho4', 'sigma4'], False),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.FROM_FIRST, [
         'xi4', 'omicron4', 'pi4', 'rho4', 'sigma4'], False),  # exact if exists
        (209, MatchMode.EXACT, SearchMode.FROM_LAST, [
         'eta7', 'theta7', 'iota7', 'kappa7', 'lambda7'], False),
        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_LAST, [
         'gamma3', 'delta3', 'epsilon3', 'zeta3', 'eta3'], False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_LAST, [
         'zeta6', 'eta6', 'theta6', 'iota6', 'kappa6'], False),
        (209, MatchMode.NEXT_LARGER, SearchMode.FROM_LAST, [
         'eta7', 'theta7', 'iota7', 'kappa7', 'lambda7'], False),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.FROM_LAST, [
         'eta7', 'theta7', 'iota7', 'kappa7', 'lambda7'], False),  # exact if exists
        (209, MatchMode.EXACT, SearchMode.BINARY_FROM_FIRST,
         ['xi4', 'omicron4', 'pi4', 'rho4', 'sigma4'], True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_FIRST,
         ['gamma3', 'delta3', 'epsilon3', 'zeta3', 'eta3'], True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_FIRST,
         ['zeta6', 'eta6', 'theta6', 'iota6', 'kappa6'], True),
        (209, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_FIRST, [
         'xi4', 'omicron4', 'pi4', 'rho4', 'sigma4'], True),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_FIRST, [
         'xi4', 'omicron4', 'pi4', 'rho4', 'sigma4'], True),  # exact if exists
        (209, MatchMode.EXACT, SearchMode.BINARY_FROM_LAST, [
         'eta7', 'theta7', 'iota7', 'kappa7', 'lambda7'], True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_LAST, [
         'gamma3', 'delta3', 'epsilon3', 'zeta3', 'eta3'], True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_LAST,
         ['zeta6', 'eta6', 'theta6', 'iota6', 'kappa6'], True),
        (209, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_LAST, [
         'eta7', 'theta7', 'iota7', 'kappa7', 'lambda7'], True),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_LAST, [
         'eta7', 'theta7', 'iota7', 'kappa7', 'lambda7'], True),  # exact if exists
    ]
)
def test_xlookup(data, lookup_value, match_mode,
                 search_mode, expected_result, should_sort):
    """Test xlookup with multiple combinations of match and search modes."""
    # Use the fixture-provided array
    # TODO: Ensure this handles horizontal orientation
    numeric_lookup_array = np.array([i for i, _ in data])
    text_return_array = np.array([t for _, t in data])
    sort_indices = np.argsort(numeric_lookup_array, None)
    lookup_array = numeric_lookup_array[sort_indices] if should_sort else numeric_lookup_array
    return_array = text_return_array[sort_indices] if should_sort else text_return_array

    # Perform the test
    assert np.all(xlookup(
        lookup_value=lookup_value,
        lookup_array=lookup_array,
        return_array=return_array,
        match_mode=match_mode,
        search_mode=search_mode
    ) == expected_result)
