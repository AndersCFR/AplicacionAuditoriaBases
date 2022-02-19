/************************************************ 2. TRIGGERS DESHABILITADOS ************************************************/
CREATE PROCEDURE TriggersDeshabilitados
AS
BEGIN
	SET NOCOUNT ON
	SELECT
		OBJECT_NAME(te.object_id) as 'Trigger',
		te.type_desc as 'On',
		OBJECT_NAME(t.parent_id) as 'Tabla',
		t.is_disabled as '¿Deshabilitado?'
	FROM sys.trigger_events te
	JOIN sys.triggers t
		ON te.object_id = t.object_id
	WHERE is_disabled = 1
END