\# Milestone 4 - Member 1

\# QA Bug Report



\## 1. Testing Summary



The Milestone 3 malware classification and threat detection pipeline was tested as part of Milestone 4 Application Testing and QA.



A total of \*\*25 automated QA tests\*\* were executed.



| Test Area | Tests | Passed | Failed |

|---|---:|---:|---:|

| Behavioral Analysis | 6 | 6 | 0 |

| ML Prediction | 4 | 4 | 0 |

| Threat Prediction | 5 | 5 | 0 |

| Threat Report | 2 | 2 | 0 |

| End-to-End Pipeline | 1 | 1 | 0 |

| Edge Cases | 4 | 4 | 0 |

| Error Handling | 3 | 3 | 0 |

| \*\*Total\*\* | \*\*25\*\* | \*\*25\*\* | \*\*0\*\* |



\---



\## 2. Bugs / Issues Identified During QA



\### BUG-01: Incorrect PowerShell test input



\*\*Component:\*\* Behavioral Analysis



\*\*Severity:\*\* Low



\*\*Description:\*\*  

The initial QA test supplied PowerShell indicators through the `suspicious\_apis` input. The implementation detects the tested PowerShell indicators through extracted strings.



\*\*Observed Result:\*\*  

The PowerShell test initially failed.



\*\*Resolution:\*\*  

The test case was corrected to provide PowerShell indicators through `extracted\_strings`.



\*\*Final Result:\*\*  

Test passed after correction.



\*\*Status:\*\* Resolved



\---



\### BUG-02: Incorrect `predict\_threat()` function call



\*\*Component:\*\* End-to-End Pipeline



\*\*Severity:\*\* Medium



\*\*Description:\*\*  

The initial end-to-end QA test passed the complete ML result dictionary to `predict\_threat()`.



The actual function requires three arguments:



```text

ml\_prediction

ml\_confidence

behavioral\_result

