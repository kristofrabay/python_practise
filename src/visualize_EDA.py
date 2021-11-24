from src.import_packages import *

class vEDA:


    """Visualize EDA - build in universal plotting functions 

    Functions can be applied on a Pandas DataFrame

    Attributes
    ----------
    data : Pandas DataFrame
        Pandas type dataframe for which the EDA plots will be created   

    Methods
    -------
    plot_corr()
        Plots the correlation matrix calculated on selected (or all) numeric features
    plot_scatter()
        Plots scatter for 2 selected features
    plot_dist()
        Plots histogram for selected 1 feature
    plot_boxplot()
        Plots the distribution of x with regards to y's categories
    plot_geo_map()
        Plots geo data (lat/lon pairs) on Plotly Express map object
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def __str__(self) -> str:
        return 'EDA visualizations for given Pandas DataFrame'

    def __repr__(self) -> str:
        return 'vEDA Object'

    def plot_corr(self, numerics = [], figsize = (18, 10)) -> plt:

        if len(numerics) == 0:
            numerics = self.data.select_dtypes(exclude = 'O').columns
    
        fig, ax = plt.subplots(figsize = figsize)
        sns.heatmap(self.data[numerics].corr(), ax = ax, cmap = 'coolwarm', center = 0, 
                    annot = True, fmt = '.2g', annot_kws={'size' : 8})
        plt.title('Correlations\n')
        plt.show()

    def plot_scatter(self, x, y, figsize = (10, 5)) -> plt:

        kwargs  =   {'edgecolor' : "k", 'linewidth' : 3/4}

        plt.figure(figsize = figsize)
        sns.scatterplot(data = self.data, x = x, y = y, s = 30, color = 'blue', legend = False, **kwargs)
        plt.title('Relationship between ' + x + ' and ' + y)
        plt.show() 

    def plot_dist(self, x, figsize = (10, 5)) -> plt:    

        plt.figure(figsize = figsize)
        sns.distplot(self.data[x], kde = False, bins = 40, hist_kws = {'edgecolor' : 'black', 'linewidth' : 1, 'alpha' : 3/4})
        plt.title('Distribution of ' + x)
        plt.xlabel(None)
        plt.ylabel(None)
        plt.show() 

    BOXPLOT_PROPS = {

        'boxprops':{'edgecolor':'black', 'linewidth' : 1},
        'flierprops':{'markerfacecolor':'black', 'markeredgecolor':'darkgray', 'marker' : 'x'},
        'medianprops':{'color':'black', 'linewidth' : 1},
        'whiskerprops':{'color':'black', 'linewidth' : 1},
        'capprops':{'color':'black', 'linewidth' : 1}

    }
   
    
    def plot_boxplot(self, x, y, figsize = (10, 5)) -> plt:

        _data = self.data.copy()

        _data[y] = _data[y].astype(str)    
        order = _data.loc[:,[x, y]].groupby([y]).median().sort_index()

        plt.figure(figsize = figsize)
        sns.boxplot(data = _data, x = x, y = y, color = 'blue', fliersize = 2, **self.BOXPLOT_PROPS, order = order.index)
        plt.ylabel(y)
        plt.xlabel(x)
        #plt.xticks(rotation = 90, ha = 'center')
        plt.title('Distribution of ' + x + ' with regards to ' + y)
        plt.show()

    def plot_geo_map(self, lat_coord, lon_coord, color_by = None, hover_name = None, hover_data = None, zoom = 5, w = 950, h = 750, title = None) -> px:
    
        self.data['size_for_plot'] = 10

        fig = px.scatter_mapbox(self.data, lat = lat_coord, lon = lon_coord, hover_name = hover_name, 
                                center = {"lat": self.data[lat_coord].mean(), "lon": self.data[lon_coord].mean()}, 
                                hover_data = hover_data, color = color_by, title = title, zoom = zoom, size_max = 5, 
                                size = 'size_for_plot', mapbox_style = 'carto-positron', width = w, height = h)
        fig.show()

        self.data.drop('size_for_plot', 1, inplace = True)