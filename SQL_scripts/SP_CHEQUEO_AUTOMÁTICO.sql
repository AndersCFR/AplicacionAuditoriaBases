/************************************************ 3. CHEQUEO AUTOMÁTICO ************************************************/
CREATE PROCEDURE ChequeoAutomatico
AS
BEGIN
	SET NOCOUNT ON
	CREATE TABLE DatosAnomalos (
		Tabla VARCHAR(100),
		[Restriccion de FK] VARCHAR(100),
		[Valor anomalo] VARCHAR(100)
	)
	INSERT INTO DatosAnomalos EXEC('DBCC CHECKCONSTRAINTS WITH ALL_CONSTRAINTS')
	SELECT * FROM DatosAnomalos
	DROP TABLE DatosAnomalos
END
