> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/hexis-verifica/evidenze/LEGGIMI_evidenze.md`, SHA-256 `9c3e3025210962249c4ba5db7e7e3c7af0893a1b420cca94e0e27d7794d23d06`.
> Translated on 2026-09-25. Structure, values and identifiers follow the original, including file names and the commands in code blocks; numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# Evidence of the consolidated review

These files accompany the report of 15 September 2026. They apply no methodological changes to the repository and do not contain the raw data.

## Contents

- `input_verificati.json`: identity of the materials examined; 33 hashes of the current package and 103 of the historical archive verified without discrepancies.
- `corpus_audit.json`, `audit_corpus.md`: counts reconstructed from the CoNLL-U files, merging and checks of the two Athenaeus XML files.
- `audit_repository.md`: checks of the actual state and transcription of the pytest outcome. It is not a complete log of the suite.
- `audit_matematico.md`, `controlli_matematici.txt`: reading of the pilots and small independent synthetic checks.
- `sintetici_25.json`: re-execution of the 25 small cases of the plan; all prescribed thresholds satisfied, including CE strictly below 0.02 for the cycle.
- `verifica_corpus.py`, `verifica_matematica.py`, `verifica_sintetici.py`: repeatable checks without new real fits. The two mathematical scripts use the reference of the attachments, not the canonical model still to be implemented.

The reports of the separate audits keep the temporary paths of the session as historical provenance. The copies and scripts present here are the evidence to be kept. In case of an interpretive difference, the main document contains the consolidated verdict.

## Repeating the checks

Use Python 3.12 and the NumPy of the repository lock (2.5.1 in the check). The census uses only the standard library.

1. For the corpus, give the script the repository with the three raw files already present and the original operational ZIP:

   ```text
   python verifica_corpus.py --repo /percorso/hexis --zip /percorso/HEXIS_allegati_operativi_v3_2026-09-11.zip
   ```

   The JSON result goes to standard output. It does not recompute the metadata of the upstream XML files: those checks are documented separately in the corpus report.

2. For the mathematics, extract the original ZIP into a working folder. Separately extract its `verifiche_CTW_precedenti.zip`. Give the outer folder `HEXIS_v3_allegati` and the inner one `ctw_validation`:

   ```text
   python verifica_matematica.py /percorso/HEXIS_v3_allegati /percorso/storico/ctw_validation
   ```

   The script reads the already existing pilots and runs only small synthetic fits. The output is numerical; the script keeps the assertion on the rational case. The observed results of the session are in `controlli_matematici.txt`.

3. For the 25 small synthetics, give the historical folder and a **new** output path:

   ```text
   python verifica_sintetici.py /percorso/storico/ctw_validation /percorso/nuovo_risultato.json
   ```

   The script fails on a violated threshold, a mutation of the model during evaluation or an already existing output file. It does not read the CoNLL-U files.

*[Translator's note: in the commands, `/percorso/` means "/path/", `storico` "historical" and `nuovo_risultato` "new result".]*

## Scope

The 120 enumeration cases and the larger earlier proofs remain evidence of the original package, verified for integrity. The small rational case and the 25 synthetics documented here are checks of the present review. They are not confused with acceptance tests passed by the future implementation of the repository.

The new census confirms the source values. It does not measure the effect of the merging on the real scores: that evaluation belongs to the future campaign after the migration of the contract.
