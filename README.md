# File-Parser
A basic file parser tool that allows for csv files etc to be parsed with custom defined rules

## Input: 
* A csv file to parse 

* a file describing the rules for each column of the file to parse 

## Output:
* A csv file containing all entries that passed all rules set 

* A csv file containing all entries that failed one or more rules

---

## Available Rules

Each row in the rules file corresponds to a column in the input file (row 1 = column 1, row 2 = column 2, etc.).
Multiple rules for a column are **semicolon (`;`) separated**.
Rules that accept multiple values (like `Has` or `HasExact`) use **comma-separated lists**.

---

###  Rule List

**`Has`**

* Passes if the column value **contains any** of the listed values (partial match)
* Multiple allowed values: comma-separated

**Example:**

```
Has:error,fail
```

---

**`HasExact`**

* Passes if the column value **exactly matches** any of the listed values
* Multiple allowed values: comma-separated

**Example:**

```
HasExact:OK,SUCCESS
```

---

**`DoesNotHave`**

* fails if the column value **contains any** of the listed values (partial match)
* Multiple allowed values: comma-separated

**Example:**

```
DoesNotHave:error,fail
```

**`IsType`**

* Passes if the column value **is of the specified type** or can be safely converted
* Examples: `Integer`, `Float`, `String`, `Boolean`

**Example:**

```
IsType:Integer
```

---

**`IsEmpty`**

* Passes if the column value is **empty**, `null`, or whitespace

**Example:**

```
IsEmpty:true
```

---

**`IsOutlier`**

* Passes if the value’s **outlier status matches the rule**
* Uses **IQR (Interquartile Range)**
* Only for numeric columns

**Examples:**

```
IsOutlier:true   → value must be an outlier  
IsOutlier:false  → value must NOT be an outlier
```

---

**`IsFreqOutlier`**

* Passes if the value’s **frequency outlier status matches the rule**
* Uses IQR on the counts of values in the column
* Works best for **categorical or discrete data**

**Examples:**

```
IsFreqOutlier:true    → value frequency must be an outlier  
IsFreqOutlier:false   → value frequency must NOT be an outlier
```

---

### Example Rules File

Each line = column, multiple rules separated by `;`:

```
Has:error,fail;IsType:String
HasExact:OK,SUCCESS;IsEmpty:false
IsType:Integer;IsOutlier:false
IsOutlier:true;IsFreqOutlier:false
```

* Line 1 → Column 1 rules
* Line 2 → Column 2 rules
* etc.

---
## Usage Instructions

* create rules.txt file with rules for each column of your input csv file 
* call parser via commandline with input and rules files 
```
python fileparser.py input.csv rules.txt 
```
* output files will be generated automatically based on the written rules 
---
