from gsrest.util.id_group import calculate_id_group_with_overflow

# |           original|     ref_py|original_group|    ref_int| ref_double|           div_spark|           div_scala|    floor_spark|floor_scala_int|   ok|
# |9223372036854775807| 1566804069|    1566804069| 1566804069| 1566804069|9.223372036854776E14|9.223372036854776E14|922337203685477|922337203685477| true|
# | 178442263217569973|-1362793124|   -1362793123|-1362793124|-1362793123|  1.7844226321757E13|  1.7844226321757E13| 17844226321757| 17844226321756|false|
# | 178442263217569972|-1362793124|   -1362793123|-1362793124|-1362793123|  1.7844226321757E13|  1.7844226321757E13| 17844226321757| 17844226321756|false|
# | 178442263217569971|-1362793124|   -1362793123|-1362793124|-1362793123|  1.7844226321757E13|  1.7844226321757E13| 17844226321757| 17844226321756|false|
# | 178442263217569974|-1362793124|   -1362793123|-1362793124|-1362793123|  1.7844226321757E13|  1.7844226321757E13| 17844226321757| 17844226321756|false|
# | 178442263217579972|-1362793123|   -1362793123|-1362793123|-1362793123|1.784422632175799...|1.784422632175799...| 17844226321757| 17844226321757| true|
# | 178442263217579973|-1362793123|   -1362793123|-1362793123|-1362793123|1.784422632175799...|1.784422632175799...| 17844226321757| 17844226321757| true|
# | 178442263217579974|-1362793123|   -1362793123|-1362793123|-1362793123|1.784422632175799...|1.784422632175799...| 17844226321757| 17844226321757| true|
# | 178442263217559972|-1362793125|   -1362793125|-1362793125|-1362793125|1.784422632175599...|1.784422632175599...| 17844226321755| 17844226321755| true|
# | 178442263217559973|-1362793125|   -1362793125|-1362793125|-1362793125|1.784422632175599...|1.784422632175599...| 17844226321755| 17844226321755| true|
# | 178442263217559974|-1362793125|   -1362793125|-1362793125|-1362793125|1.784422632175599...|1.784422632175599...| 17844226321755| 17844226321755| true|
# |         2147483647|     214748|        214748|     214748|     214748|         214748.3647|         214748.3647|         214748|         214748| true|
# |         2147483648|     214748|        214748|     214748|     214748|         214748.3648|         214748.3648|         214748|         214748| true|
# |         2147483646|     214748|        214748|     214748|     214748|         214748.3646|         214748.3646|         214748|         214748| true|
# |         4294967295|     429496|        429496|     429496|     429496|         429496.7295|         429496.7295|         429496|         429496| true|
# |         4294967296|     429496|        429496|     429496|     429496|         429496.7296|         429496.7296|         429496|         429496| true|
# |         4294967294|     429496|        429496|     429496|     429496|         429496.7294|         429496.7294|         429496|         429496| true|
# |     21474836470000| 2147483647|    2147483647| 2147483647| 2147483647|       2.147483647E9|       2.147483647E9|     2147483647|     2147483647| true|
# |     21474836470001| 2147483647|    2147483647| 2147483647| 2147483647|   2.1474836470001E9|   2.1474836470001E9|     2147483647|     2147483647| true|
# |     21474836469999| 2147483646|    2147483646| 2147483646| 2147483646|   2.1474836469999E9|   2.1474836469999E9|     2147483646|     2147483646| true|
# |     21474836470002| 2147483647|    2147483647| 2147483647| 2147483647|   2.1474836470002E9|   2.1474836470002E9|     2147483647|     2147483647| true|
# |     21474836469998| 2147483646|    2147483646| 2147483646| 2147483646|   2.1474836469998E9|   2.1474836469998E9|     2147483646|     2147483646| true|
# |     42949672950000|         -1|            -1|         -1|         -1|       4.294967295E9|       4.294967295E9|     4294967295|     4294967295| true|
# |     42949672960000|          0|             0|          0|          0|       4.294967296E9|       4.294967296E9|     4294967296|     4294967296| true|
# |     42949672940000|         -2|            -2|         -2|         -2|       4.294967294E9|       4.294967294E9|     4294967294|     4294967294| true|
# |                  1|          0|             0|          0|          0|              1.0E-4|              1.0E-4|              0|              0| true|
# |               1000|          0|             0|          0|          0|                 0.1|                 0.1|              0|              0| true|
# |             100000|         10|            10|         10|         10|                10.0|                10.0|             10|             10| true|


def test_compute_tx_id_group():
    original = [
        9223372036854775807,
        178442263217569973,
        178442263217569972,
        178442263217569971,
        178442263217569974,
        178442263217579972,
        178442263217579973,
        178442263217579974,
        178442263217559972,
        178442263217559973,
        178442263217559974,
        2147483647,
        2147483648,
        2147483646,
        4294967295,
        4294967296,
        4294967294,
        21474836470000,
        21474836470001,
        21474836469999,
        21474836470002,
        21474836469998,
        42949672950000,
        42949672960000,
        42949672940000,
        1,
        1000,
        100000,
    ]

    ref = [
        1566804069,
        -1362793123,
        -1362793123,
        -1362793123,
        -1362793123,
        -1362793123,
        -1362793123,
        -1362793123,
        -1362793125,
        -1362793125,
        -1362793125,
        214748,
        214748,
        214748,
        429496,
        429496,
        429496,
        2147483647,
        2147483647,
        2147483646,
        2147483647,
        2147483646,
        -1,
        0,
        -2,
        0,
        0,
        10,
    ]

    # for o, r in zip(original, ref):
    #     if calculate_id_group_with_overflow(o, 10000) != r:
    #         print(calculate_id_group_with_overflow(o, 10000),r)
    assert all(
        [calculate_id_group_with_overflow(o, 10000) == r for o, r in zip(original, ref)]
    )

    # check that results are unsigned
    assert calculate_id_group_with_overflow(25688199397376, 10000) != 2568819939
    assert calculate_id_group_with_overflow(25688199397376, 10000) == -1726147357
