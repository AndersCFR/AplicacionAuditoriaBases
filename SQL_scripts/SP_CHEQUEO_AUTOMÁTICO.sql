/************************************************ 3. CHEQUEO AUTOM�TICO ************************************************/
CREATE PROCEDURE ChequeoAutomatico
AS
BEGIN
	SET NOCOUNT ON
	CREATE TABLE DatosAnomalos (
		Tabla VARCHAR(100),
		[Restriccion] VARCHAR(100),
		[Valor anomalo] VARCHAR(100)
	)
	INSERT INTO DatosAnomalos EXEC('DBCC CHECKCONSTRAINTS WITH ALL_CONSTRAINTS')
	SELECT * FROM DatosAnomalos
	DROP TABLE DatosAnomalos
END
