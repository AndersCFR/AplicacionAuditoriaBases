/************************************************ 1.2. POSIBLES RELACIONES ************************************************/
CREATE PROCEDURE PosiblesRelaciones
AS
BEGIN
	SET NOCOUNT ON
	/* Tabla temporal: Encontrar PK */
	SELECT 
		tablas.name as 'Tabla',
		col.name as 'Columna PK'
	INTO Claves_Primarias
	FROM sys.tables tablas JOIN sys.indexes pk
		ON tablas.object_id = pk.object_id
		AND pk.is_primary_key = 1
	JOIN sys.index_columns ic
		ON ic.object_id = pk.object_id
		AND ic.index_id = pk.index_id
	JOIN sys.columns col
		ON pk.object_id = col.object_id
		AND col.column_id = ic.column_id
	WHERE tablas.name != 'sysdiagrams'
	AND tablas.name != 'ClavesPrimarias'

	/* Tabla temporal: Columnas existentes en cada tabla */
	SELECT
		tab.name as table_name,
		col.name as column_name, 
		t.name as data_type
	INTO columnas
	FROM sys.tables tab
		JOIN sys.columns as col
			ON tab.object_id = col.object_id
		LEFT JOIN sys.types as t
			ON col.user_type_id = t.user_type_id
	WHERE tab.name != 'sysdiagrams'


	/* Obtener columnas que se repiten en otras tablas y sus posibles relaciones inexistentes */
	SELECT
		table_name as 'Tabla',
		column_name as 'Columna',
		Tablas as 'Tablas donde la columna es PK'
	FROM (
		/* Columnas que no apuntan a un padre y al tener nombres similares pueden implicar que falta una relación */
		SELECT
			table_name, column_name
		FROM (
			/* Columnas que tienen más de 1 ocurrencia con su respectiva tabla */
			SELECT
				columnas.column_name,
				columnas.table_name
			FROM (
				/* Columnas que tienen más de 1 ocurrencia */
				SELECT column_name FROM columnas
				GROUP BY column_name
				HAVING COUNT(*) > 1
			) columnas_repetidas
			JOIN (
				SELECT * FROM columnas
			) columnas
			ON columnas_repetidas.column_name = columnas.column_name
			) posibles_relaciones
		FULL JOIN (
			/* Restricciones de clave foránea con sus respectivas columnas */
			SELECT
				fk_tab.name as 'Tabla Hijo',
				pk_tab.name as 'Tabla Padre', 
				fk_col.name as 'Columna FK',
				pk_col.name as 'Columna PK',
				fk.name as 'Restriccion'
			FROM sys.foreign_keys fk
				JOIN sys.tables fk_tab
					ON fk_tab.object_id = fk.parent_object_id
				JOIN sys.tables pk_tab
					ON pk_tab.object_id = fk.referenced_object_id
				JOIN sys.foreign_key_columns fk_cols
					ON fk_cols.constraint_object_id = fk.object_id
				JOIN sys.columns fk_col
					ON fk_col.column_id = fk_cols.parent_column_id
					AND fk_col.object_id = fk_tab.object_id
				JOIN sys.columns pk_col
					ON pk_col.column_id = fk_cols.referenced_column_id
					AND pk_col.object_id = pk_tab.object_id
		) claves_foraneas
		ON posibles_relaciones.column_name = claves_foraneas.[Columna FK]
		AND (
			posibles_relaciones.table_name = claves_foraneas.[Tabla Hijo]
			OR
			posibles_relaciones.table_name = claves_foraneas.[Tabla Padre]
		)
		WHERE Restriccion is NULL
	) columnas_posibles
	LEFT JOIN (
		/* Claves primarias y sus tablas */
		SELECT
			[Columna PK],
			/* Concatenación de los nombres de las tablas */
			STUFF((
				SELECT ', ' + Tabla
				FROM Claves_Primarias
				WHERE [Columna PK] = claves.[Columna PK]
				FOR XML PATH(''), TYPE).value('(./text())[1]','VARCHAR(MAX)')
			,1,2,'') as Tablas
		FROM Claves_Primarias claves
		GROUP BY [Columna PK]
	) pk_tablas
	/* Se buscan tablas con las que podría necesitarse una relación */
	ON columnas_posibles.column_name = pk_tablas.[Columna PK]
	ORDER BY column_name

	/* Eliminar tablas temporales */
	DROP TABLE columnas
	DROP TABLE Claves_Primarias
END