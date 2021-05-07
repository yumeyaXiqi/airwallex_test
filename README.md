# Run
run all case: pytest test_bank.py   
run one class: pytest test_bank.py::Test_Bank_Negative

# parameters
 If you need log: --capture=no -o log_cli=true -o log_cli_level=INFO   
 If you need change bank url: --bank_url xxx

# Env
 python3.7   
 pip3 install pytest
