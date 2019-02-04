CREATE DEFINER=`usrRLCY_ETL`@`%` PROCEDURE `TruncateTables`()
BEGIN
truncate table BillingDetail
;
truncate table BillingSummary
;
truncate table ContractSummary
;
truncate table `Non Reimb`
;
truncate table OracleDataAllow
;
truncate table `OracleDataT&M`
;
truncate table ProjectsSummary
;
truncate table `Subtask reference`
;
END