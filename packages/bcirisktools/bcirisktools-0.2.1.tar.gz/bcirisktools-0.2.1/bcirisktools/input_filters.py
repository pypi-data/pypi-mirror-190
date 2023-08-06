# Estructura de datos
import numpy as np
import pandas as pd

import sys

# Metricas
from .metrics_bci import MetricsBCI


class InputTreatment:
    
    def __init__(self, data, variables, model_label):
        
        self.variables   = variables
        self.model_label = model_label
        self.univariate_table, self.selected_vars = self.univPredict(data, 
                                                                self.variables, 
                                                                self.model_label)
    
    def SelCorrFam(self, df_in, corThr = 0.7, method = 'pearson', family = False):
        """
        SelCorrFam es la funcion encargada de filtrar las variables 
        por el criterio de correlacion entre variables.

        Parametros de entrada: 
                data : datos por procesar
                predVar : Listado de variables.
                featuresGroups : Listado de las familias de variables.
                corThr : Corte de valor de coeficiente de correlacion 
                para la seleccion. Por defecto es 0.7.
                method : Marca 'pearson' o 'cramer', para elegir el 
                coeficiente de correlacion a usar. Por defecto es 'pearson'.

        Salida:
                predVar = Dataframe con las variables seleccionadas por 
                el filtro de correlacion.
                seleccionadas = Listado de variables seleccionadas por 
                el filtro de correlacion.

        """
        
        data = df_in.copy()
        if family:
            predVar['Group'] = 'SinGrupo'
    
        predVar, featuresGroups = self.univariate_table, self.selected_vars
        
        seleccionadas = []
        variables_revisadas     = []
        variables_seleccionadas = []
        features = predVar['Feature']
        total_variables = len(featuresGroups)
        for it, FAM in enumerate(featuresGroups):    
            sys.stdout.write(f'\rVariable analizada: {FAM} \t [{it+1}/{total_variables}]')
            famlist = [k for k in features if FAM in k]
            if FAM == 'SinGrupo':
                predVarFam = predVar.sort_values('KS', ascending = False)
            else:
                predVarFam = predVar.loc[predVar['Feature'].isin(famlist),:].sort_values('KS', ascending = False)

            variables_candidatas    = predVarFam['Feature']

            corMtx = data.loc[:, variables_candidatas].corr(method = method)

            for f in variables_candidatas:
                if f not in variables_revisadas:
                    variables_revisadas.append(f)
                    #variables_seleccionadas.append(f)

                    corTemp = list(corMtx.index[(np.abs(corMtx[f]) < corThr)])
                    variables_seleccionadas = variables_seleccionadas + corTemp

        seleccionadas = list(np.unique(variables_seleccionadas))
        predVar = predVar.loc[predVar['Feature'].isin(seleccionadas),:]

        print(f"\nVariables candidatas iniciales: {len(self.selected_vars)}")
        print(f"\nSeleccionadas por correlación familiar: {len(seleccionadas)}")

        return predVar, seleccionadas, variables_seleccionadas
    
    def FiltCorr(self, df_in, corThr = 0.7, method = 'pearson', family = False):
        
        predVar = self.univariate_table
        if family:
            predVar['Group'] = 'SinGrupo'
            
        selected_variables = []
        for group in predVar['Group'].unique():
            variables = predVar[predVar['Group'] == group]['Feature']
            selected_variables.append(self._identify_correlated(df_in[variables], 0.9))
        seleccionadas = self._flatten(selected_variables)
        
        print(f"\nVariables candidatas iniciales: {len(self.selected_vars)}")
        print(f"\nSeleccionadas por correlación familiar: {len(seleccionadas)}")
        return seleccionadas
    
    @staticmethod
    def univPredict(df_in, variables, model_label):
        
        data_model = df_in.copy()
        predVar = []
        total_variables = len(variables)

        for it, f in enumerate(variables):
            sys.stdout.write(f'\rProcesando [{it+1}/{total_variables}]' + "\r")
            metricas = MetricsBCI.evaluate(data_model[model_label], data_model[f].astype(float))
            grupo_var = f.split("_")[0]
            predVar.append([f, grupo_var, metricas[0],metricas[1],metricas[2]])
            
        predVar = pd.DataFrame(predVar, columns = ['Feature','Group','ROC','KS','DIV'])

        # En base a criterios de KS y ROC se selecciona las Variables que sobrepasen un valor al ser consideradas predictivas.
        print(f"Variables candidatas iniciales: {len(variables)}", )
        predVar_filtered       = predVar.loc[(predVar['KS'] > 0.01) & (predVar['ROC'] > 0.501),:]
        seleccionadas          = list(predVar_filtered['Feature'].values)
        print(f"\nSeleccionadas por univariado: {len(seleccionadas)}")
        
        return predVar_filtered, seleccionadas
    
    @staticmethod
    def filldata(df_in, 
                 num_value=-999999, 
                 cat_value='unk'):
        
        data = df_in.copy()   
        for col in data.columns:
            try:
                data[col] = data[col].fillna(num_value)
            except:
                data[col] = data[col].cat.add_categories(cat_value)
                data[col] = data[col].fillna(cat_value, inplace =True)
        
        return data
    
    @staticmethod
    def _flatten(l):
        return [item for sublist in l for item in sublist]
    
    @staticmethod
    def _identify_correlated(df, threshold):
        """
        A function to identify highly correlated features.
        """
        # Compute correlation matrix with absolute values
        matrix = df.corr(method = "spearman").abs()

        # Create a boolean mask
        mask = np.triu(np.ones_like(matrix, dtype=bool))

        # Subset the matrix
        reduced_matrix = matrix.mask(mask)

        # Find cols that meet the threshold
        to_drop = [c for c in reduced_matrix.columns if \
                  not any(reduced_matrix[c] > threshold)]

        return to_drop