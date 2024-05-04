from topsort import Graph

pp_max_len = 50

test_idx = 0
succ_count = 0
fail_count = 0

def _pp(fstr, center=False):
    def pp_aux(fstr, center):
        while len(fstr) <= pp_max_len:
            fstr = f"""{" " if center else ""}{fstr} """
        fstr = fstr[:pp_max_len]
        print(f"|{fstr}|")

    newline = fstr.find("\n")
    if newline == -1:
        pp_aux(fstr, center)
    else:
        pp_aux(fstr[:newline], center)
        _pp(fstr[newline+1:], center)

def _test(rels, expected_order, test_name=""):
    global test_idx
    i = test_idx
    test_idx += 1
    g = Graph(rels_input=rels, debug=False)
    actual_order = g.topsort()

    if expected_order != actual_order:
        global fail_count
        fail_count += 1
        return f"""[x] Test {i} {"- " + test_name if test_name else ""}
    [√] => {expected_order}
    [?] => {actual_order}"""
    
    global succ_count
    succ_count += 1
    return f"""[√] Test {i} {"- " + test_name if test_name else ""}"""

def run_test_suite(*tests):
    suite = [t() for t in tests]

    _pp("====================================================================")
    _pp("TEST SUMMARY:", center=True)
    _pp("--------------------------------------------------------------------")
    _pp(f"[√ SUCCESS] => {succ_count}")
    _pp(f"[x FAILURE] => {fail_count}")
    _pp("====================================================================")
    _pp("TEST DETAILS:", center=True)
    _pp("--------------------------------------------------------------------")
    for result in suite:
        _pp(result)
    _pp("____________________________________________________________________")


def test_empty_graph():
    rels = ""
    result = _test(rels, [], test_name="Empty graph")
    return result

def test_single_rel():
    rels = "A>B"
    result = _test(rels, ["A", "B"], test_name="Single relationship")
    return result

def test_simple_graph():
    rels = "A>B,B>C,B>D,D>E,C>E"
    exp = ["A", "B", "D", "C", "E"]
    result = _test(rels, exp, test_name="Simple graph")
    return result

def main():
    run_test_suite(
        test_empty_graph, 
        test_single_rel,
        test_simple_graph,
    )

if __name__ == "__main__":
    main()
