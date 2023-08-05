################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R
# (c) Copyright IBM Corp. 2020, 2022. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

#Chek if autoai4ml_ts is available if not then set tslibs
try:
    import ai4ml_ts
except:
    import sys
    from autoai_ts_libs import watfore
    sys.modules['ai4ml_ts'] = watfore
    sys.modules['ai4ml_ts.estimators'] = watfore