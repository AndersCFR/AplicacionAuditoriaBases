/************************************************ 1.1. RELACIONES DESHABILITADAS ************************************************/
CREATE PROCEDURE RelacionesDeshabilitadas
AS
BEGIN
	SET NOCOUNT ON
	SELECT
		name as 'Relacion',
		OBJECT_NAME(parent_object_id) as 'Tabla hijo',
		OBJECT_NAME(referenced_object_id) as 'Tabla padre',
		is_disabled as '�Deshabilitado?'
	FROM sys.foreign_keys
	WHERE is_disabled = 1
END