# Metric Card for [Metric Name]

## Table of Contents
- Metric Description(#metric-description)
    - Metric Summary
        - Possible Values
        - Requires Reference/'ground truth'?
    - Supported Tasks and Leaderboards
    - Possible Values
    - Languages Supported
- Metric Use
    - Inputs
    - Outputs
    - Examples
- Considerations for Using the Metric
    - Social Impact of the Metric
    - Discussion of Biases
    - Other Known Limitations
    - Reproducibility Considerations
- Mathematical Foundations
    - Equation(s)
    - Mathematical Context
    - Additional Resources
- Metric Creation?? (find title for this!)
    - Curation Rationale
    - Source Data (if applicable)
    - Related Metrics (if applicable)
- Additional Information
    - Licensing Information
    - Citation Information
    - Contributions

---

## Metric Description
- **Homepage:**
- **Repository:**
- **Paper:**
- **Point of Contact:**


### Metric Summary
- A predicted string's exact match value is 1 if it is the exact same as the reference, and is 0 otherwise.
    - Example 1: The exact match score of prediction "Happy Birthday!" is 0, given its reference is "Happy New Year!".
    - Example 2: The exact match score of prediction "The Colour of Magic (1983)" is 1, given its reference is also "The Colour of Magic (1983)".
- The exact match score of a set of predictions is the sum of all of the individual exact match scores in the set, divided by the total number of predictions in the set, and then multiplied by 100.

#### Possible Values
- 0 to 100, inclusive 
    - (i.e. it can be any number from 0 to 100, including 0 and 100)
#### Requires Reference/'ground truth'?
Yes. Exact match requires an input 'ground truth' reference for each input prediction.

### Supported Tasks and Leaderboards
Tasks: Any task where two strings are compared.
Leaderboards: None.

### Languages Supported
All lanugages are supported, as long as there is a 'ground truth' reference to compare each input against.

## Metric Use
### Inputs
### Outputs
### Examples

## Considerations for Using the Metric

### Social Impact of the Metric
- works better with good data, good data is often more likely to appear for groups/cases/instances with more resources

### Discussion of Biases
- ??

### Other Known Limitations
- doesn't capture meaning or anything close to correct–if there is one slight thing wrong, it's all marked as incorrect; no middle ground/partial credit

### Reproducibility Considerations
- what characters don't have to be the same
    - this paper ignores punctuation and articles if they're different (https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1174/reports/2761899.pdf)
        - e.g. "the cat sat!" and "a cat sat." would be marked as exact matches, with a score of 1
- what device this metric is calculated on
    - e.g. cpu, different types of gpus
- general things:
    - what version of the repo is being used?
    - 

## Mathematical Foundations
### Equation(s)
$
score = \frac{\sum_{(p,r)\in N}{match(p,r)}}{\lvert N\rvert}
$
where $N$ is the set of examples, $ \lvert N\rvert $ is the total number of examples, and $match(p,r) = 1$ if the prediction ($p$) and reference ($r$) are exact matches, and $match(p,r) = 0$ if they are not.

### Mathematical Context
- N/A ?
### Additional Resources

## Metric Creation?? (find title for this!)
### Curation Rationale
### Source Data (if applicable)
### Related Metrics (if applicable)

## Additional Information
### Licensing Information
### Citation Information
### Contributions