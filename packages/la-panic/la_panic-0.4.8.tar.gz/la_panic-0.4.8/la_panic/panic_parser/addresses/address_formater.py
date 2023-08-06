def reformat_register_value_to_fit(register_value: str) -> str:
    # 16 bytes + 0x
    register_value_string_len = 18

    if len(register_value) < register_value_string_len:
        register_value = register_value.ljust(register_value_string_len)
    # elif len(register_value) > register_value_string_len:
    #     register_value = register_value[0:register_value_string_len - 3] + "..."

    return register_value
