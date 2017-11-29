import numpy as np
from trading_strategy_fitting import tic, tensorflow_offset_scan_validation, fit_tensorflow,\
    underlined_output, import_data, input_processing
from strategy_evaluation import output_strategy_results
from data_input_processing import preprocessing_inputs


def tensorflow_fitting(strategy_dictionary_local):
    toc = tic()
    data_local, data_2 = import_data(strategy_dictionary_local)
    fitting_inputs_local, continuous_targets, classification_targets = input_processing(
        data_local, data_2, strategy_dictionary)

    if strategy_dictionary_local['regression_mode'] == 'classification':
        fitting_targets_local = classification_targets
    elif strategy_dictionary_local['regression_mode'] == 'regression':
        fitting_targets_local = continuous_targets

    fitting_inputs_local, strategy_dictionary_local = preprocessing_inputs(
        strategy_dictionary_local, fitting_inputs_local)

    fitting_dictionary, error_loop, profit_factor = fit_tensorflow(
        strategy_dictionary_local,
        data_local,
        fitting_inputs_local,
        fitting_targets_local)

    underlined_output('Best strategy fit')
    output_strategy_results(strategy_dictionary, fitting_dictionary, data_local, toc)

    return strategy_dictionary, data_local, fitting_inputs_local, fitting_targets_local

if __name__ == '__main__':
    strategy_dictionary = {
        'trading_currencies': ['USDT', 'BTC'],
        'ticker_1': 'USDT_BTC',
        'ticker_2': 'BTC_ETH',
        'scraper_currency_1': 'BTC',
        'scraper_currency_2': 'ETH',
        'candle_size': 300,
        'n_days': 40,
        'offset': 0,
        'bid_ask_spread': 0.004,
        'transaction_fee': 0.0025,
        'train_test_validation_ratios': [0.5, 0.25, 0.25],
        'output_flag': True,
        'plot_flag': False,
        'target_score': 'idealstrategy',
        'windows': [10, 50, 100],
        'regression_mode': 'regression',
        'preprocessing': 'None',
        'ml_mode': 'tensorflow',
        'sequence_flag': True,
        'web_flag': True,
        'filename1': "USDT_BTC.csv",
        'filename2': "BTC_ETH.csv",
        'scraper_page_limit': 10,
    }

    strategy_dictionary, data_to_predict, fitting_inputs, fitting_targets = tensorflow_fitting(
        strategy_dictionary)

    underlined_output('Offset validation')
    offsets = np.linspace(0, 100, 5)

    tensorflow_offset_scan_validation(strategy_dictionary, data_to_predict, fitting_inputs, fitting_targets, offsets)

    print strategy_dictionary
