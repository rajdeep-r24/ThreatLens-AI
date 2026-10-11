\# Milestone 4 – Application Testing \& QA

\## ThreatLens AI



\### 1. Objective



The objective of this QA activity is to validate the Milestone 3 AI prediction,

behavioral analysis, threat prediction, threat reporting, and end-to-end

workflow of the ThreatLens AI system.



The testing focuses on functional correctness, expected threat classification,

risk scoring, recommended security actions, error handling, and workflow

validation.



\---



\## 2. Test Cases



| ID | Module | Test Scenario | Expected Result | Status |

|----|--------|---------------|-----------------|--------|

| TC-01 | Behavioral Analysis | Benign input with no suspicious indicators | No significant behavioral threat detected | Pending |

| TC-02 | Behavioral Analysis | Suspicious PowerShell indicators | PowerShell behavior detected | Pending |

| TC-03 | Behavioral Analysis | Persistence indicators | Persistence behavior detected | Pending |

| TC-04 | Behavioral Analysis | Process injection indicators | Process injection detected with Critical severity | Pending |

| TC-05 | Behavioral Analysis | Network/payload download indicators | Payload/network retrieval detected | Pending |

| TC-06 | Behavioral Analysis | Multiple malicious indicators | Multiple behaviors detected and score increased | Pending |

| TC-07 | ML Prediction | Benign sample passed to trained model | Model predicts Benign | Pending |

| TC-08 | ML Prediction | Malware sample passed to trained model | Model predicts Malware | Pending |

| TC-09 | Threat Prediction | Benign ML result with no suspicious behavior | Low threat level and monitoring action | Pending |

| TC-10 | Threat Prediction | Malware prediction with no behavioral evidence | Threat score generated correctly | Pending |

| TC-11 | Threat Prediction | Malware + process injection | Critical threat level and immediate quarantine action | Pending |

| TC-12 | Threat Prediction | Malware + multiple suspicious behaviors | High/Critical threat assessment generated | Pending |

| TC-13 | Threat Report | Generate report from threat prediction | Structured threat report generated | Pending |

| TC-14 | End-to-End | ML → Behavioral Analysis → Threat Prediction → Report | Complete workflow executes successfully | Pending |

| TC-15 | Edge Case | Empty behavioral indicators | System handles input without crashing | Pending |

| TC-16 | Error Handling | Invalid/missing model path | Appropriate error is raised | Pending |



\---



\## 3. Validation Criteria



A test case is considered PASS when:



1\. The system executes without an unexpected error.

2\. The actual output matches the expected behavior.

3\. Threat levels and recommended actions are logically consistent with

&#x20;  the implemented threat prediction rules.

4\. Generated reports contain the required threat assessment information.



\---



\## 4. QA Scope



The following components are included in testing:



\- Behavioral Analysis

\- ML Malware Prediction

\- Threat Prediction

\- Threat Scoring

\- Threat Level Classification

\- Recommended Security Actions

\- Threat Report Generation

\- End-to-End Workflow

\- Edge Cases

\- Error Handling



\---



\## 5. Test Result Summary



Total Test Cases: 16



Passed: To be updated after execution



Failed: To be updated after execution



Blocked: To be updated after execution

