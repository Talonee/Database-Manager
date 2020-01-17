# Database-Manager

The project is currently **in progress** and is expected to have four (4) components, each performing separate functions: extract, encode + decode, input, and analyze.

## Extract 
File: `extract.py` *(Completed)*

This program's purpose(s):
* Web scrape through an old web database to retrieve raw data.
* Clean, structure and enrich raw data into a desired format.
* Export data into CSV files to be used in other programs.

## Encode + Decode
File: `encode.py + decode.py`  *(Completed)*

These programs' purpose(s):
* Encode output retrieved from **Extract**.
* Decode output retrieved from **Encode**. (*decode.py is hidden*)

## Input
File: `input.py` *(Completed)*

This program's purpose(s):
* Navigate web database by web interaction.
* Read CSV files and automate filling/transferring data.
* Homogenize/Clean pre-exisiting data.
* Integrate both web scrape and web interaction.

## Analyze
File: `analyze.py` *(Null)*

This program's purpose(s):
* Create graphs and models concerning data retrieved from **Extract**.
* Determine various statistical information within the data.
* Analyze and predict data trends.

## Results
With manual entry:
`3 hrs/day * 4 days/wk * 4 wks/mo * 2 mo = 96 hrs/file * 14 files`
--> **1344 hrs / 14 files**

With Database Manager's automation:
--> **16 hrs / 14 files**

Efficiency calculation:
`100% - (16 / 1344 * 100)% = 99%`
--> **Database Manager is 99% more efficient than manual labor when it comes to time consumptions.**
