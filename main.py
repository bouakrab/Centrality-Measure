from flask import Flask, render_template, redirect, url_for, request
import matplotlib.pyplot as plt
import networkx as nx
import csv
import numpy as np
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib import gridspec
import matplotlib.patches as mpatches


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
ALLOWED_EXTENSIONS = {'csv'}

@app.route("/", methods=["POST", "GET"])
def login():
        if request.method == "POST":
            if 'log_in' in request.form :
                with open("login.csv") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if request.form['nom'] == row[0] and request.form['pass'] == row[1] :
                            return redirect(url_for("home"))
            else :
                with open("login.csv", 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if request.form['nom2'] == row[0] and request.form['pass2'] == row[1] :
                            return render_template('login.html', afficher=1)
                    with open("login.csv", 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile,delimiter=',')
                        writer.writerow([request.form['nom2'],request.form['pass2']])
                        return redirect(url_for("home",message=1)) 
            return render_template('login.html')
        else :
            return render_template('login.html')


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/home", methods=["POST", "GET"])
def home():
        if request.method == "POST":
            if request.form.get('upload') :
                uploaded_file = request.files['file']
                if uploaded_file.filename != '' and allowed_file(uploaded_file.filename) :
                    uploaded_file.save("test.csv")
                    return render_template('index.html',message='2')
                else :
                    return render_template('index.html')
            if request.form.get('post_csv') :
                return redirect(url_for("home_csv"))
        elif request.args.get('message', type=int) :
            return render_template('index.html', message=request.args['message'])
        else :
            return render_template('index.html')

            
@app.route("/home_csv", methods=["POST", "GET"])
def home_csv():
        if os.path.exists('static/assets/images/graphe.png'):
            os.remove('static/assets/images/graphe.png')
        if os.path.exists('static/assets/images/graphe_degre.png'):
            os.remove('static/assets/images/graphe_degre.png')
        if os.path.exists('static/assets/images/graphe_inter.png'):
            os.remove('static/assets/images/graphe_inter.png')
        if os.path.exists('static/assets/images/graphe_prox.png'):
            os.remove('static/assets/images/graphe_prox.png')
        if os.path.exists('static/assets/images/graphe_degre_inter.png'):
            os.remove('static/assets/images/graphe_degre_inter.png')
        if os.path.exists('static/assets/images/graphe_degre_prox.png'):
            os.remove('static/assets/images/graphe_degre_prox.png') 
        if os.path.exists('static/assets/images/graphe_inter_prox.png'):
            os.remove('static/assets/images/graphe_inter_prox.png')
        if os.path.exists('static/assets/images/graphe_degre_inter_prox.png'):
            os.remove('static/assets/images/graphe_degre_inter_prox.png')
        
        results = []
        with open("test.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                results.append(row)
        leng = len(results)
        G = nx.Graph()

        #creer les noeuds de graph
        for col in range(1,leng):
            G.add_node(results[0][col])
        
        #creer les 
        for row in range(1,leng):
            for col in range(1,leng):
                if (results[row][col] == '1'):
                        G.add_edge(results[row][0], results[0][col])
                        #print(results[row][col],"h")
        
        if request.method == "POST":
            
            if request.form.get('check-4') :
                N = int(request.form['check-4'])
            else :
                N = leng
                
                
            if 'check-1' in request.form and 'check-2' in request.form and 'check-3' in request.form :
                degre_centralite = nx.degree_centrality(G)
                centralite_inter = nx.betweenness_centrality(G)
                centralite_prox = nx.closeness_centrality(G)
                degre_centralite_sorted=dict(sorted(degre_centralite.items(), key=lambda item: item[1], reverse = True))
                centralite_inter_sorted=dict(sorted(centralite_inter.items(), key=lambda item: item[1], reverse = True))
                centralite_prox_sorted=dict(sorted(centralite_prox.items(), key=lambda item: item[1], reverse = True))

                
                degre = np.array(list(degre_centralite.values()))
                inter = np.array(list(centralite_inter.values()))
                prox = np.array(list(centralite_prox.values()))

                X = np.arange(len(degre))
                fig = plt.figure()
                ax = fig.add_axes([0.06,0.15,0.93,0.79])
                ax.bar(X -0.2, degre, color = '#808000', width = 0.2)
                ax.bar(X, inter, color = '#800000', width = 0.2)
                ax.bar(X + 0.2, prox, color = '#008080', width = 0.2)
                x_labels = np.array(list(degre_centralite.keys()))
                ax.set_xticks(X)
                ax.set_xticklabels(x_labels,rotation=45)
                title_obj = plt.title("les trois centralites")
                plt.setp(title_obj, color='b')
                
                CD = mpatches.Patch(color='#808000', label='degree centrality')
                CI = mpatches.Patch(color='#800000', label="betweenness centrality")
                CP = mpatches.Patch(color='#008080', label='closeness centrality')
                plt.legend(handles=[CD,CI,CP], loc=2,  prop={'size': 10})
                
                plt.savefig('static/assets/images/graphe_degre_inter_prox.png')
                plt.close()
                N_degre=dict(list(degre_centralite_sorted.items())[:N])
                N_inter=dict(list(centralite_inter_sorted.items())[:N])
                N_prox=dict(list(centralite_prox_sorted.items())[:N])
                return render_template('graphe.html', results=results, leng=leng, flash_message="123", D=N_degre, E=N_inter, F=N_prox)
            elif 'check-1' in request.form and 'check-2' in request.form :
                degre_centralite = nx.degree_centrality(G)
                centralite_inter = nx.betweenness_centrality(G)
                degre_centralite_sorted=dict(sorted(degre_centralite.items(), key=lambda item: item[1], reverse = True))
                centralite_inter_sorted=dict(sorted(centralite_inter.items(), key=lambda item: item[1], reverse = True))
                
                title_obj = plt.title("size-->degree centrality \n color-->betweenness centrality")
                plt.setp(title_obj, color='b')
                plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99 , top=0.9, wspace=0, hspace=0)
                
                cent = np.fromiter(centralite_inter.values(), float)
                normalize = mcolors.Normalize(vmin=cent.min(), vmax=cent.max())
                colormap = cm.summer
                scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
                scalarmappaple.set_array(centralite_inter)
                plt.colorbar(scalarmappaple,shrink=0.5)
                nx.draw(G,with_labels=True,node_size=[v * 500 + 200 for v in degre_centralite.values()], node_color=[v for v in centralite_inter.values()], cmap=colormap, linewidths=1)
                ax = plt.gca()
                ax.collections[0].set_edgecolor("#555")
                plt.savefig('static/assets/images/graphe_degre_inter.png')
                plt.close()
                
                N_degre=dict(list(degre_centralite_sorted.items())[:N])
                N_inter=dict(list(centralite_inter_sorted.items())[:N])
                return render_template('graphe.html', results=results, leng=leng, flash_message="12", D=N_degre, E=N_inter)
            elif 'check-1' in request.form and 'check-3' in request.form :
                degre_centralite = nx.degree_centrality(G)
                centralite_prox = nx.closeness_centrality(G)
                degre_centralite_sorted=dict(sorted(degre_centralite.items(), key=lambda item: item[1], reverse = True))
                centralite_prox_sorted=dict(sorted(centralite_prox.items(), key=lambda item: item[1], reverse = True))
                
                
                title_obj = plt.title("size-->degree centrality \n color-->closeness centrality")
                plt.setp(title_obj, color='b')
                plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99 , top=0.9, wspace=0, hspace=0)
                
                cent = np.fromiter(centralite_prox.values(), float)
                normalize = mcolors.Normalize(vmin=cent.min(), vmax=cent.max())
                colormap = cm.summer
                scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
                scalarmappaple.set_array(centralite_prox)
                plt.colorbar(scalarmappaple,shrink=0.5)
                nx.draw(G, with_labels=True,node_size=[v * 500 + 200 for v in degre_centralite.values()], node_color=[v for v in centralite_prox.values()], cmap=colormap, linewidths=1)
                ax = plt.gca()
                ax.collections[0].set_edgecolor("#555")
                plt.savefig('static/assets/images/graphe_degre_prox.png')
                plt.close()
                
                N_degre=dict(list(degre_centralite_sorted.items())[:N])
                N_prox=dict(list(centralite_prox_sorted.items())[:N])
                return render_template('graphe.html', results=results, leng=leng, flash_message="13", D=N_degre, E=N_prox)
            elif 'check-2' in request.form and 'check-3' in request.form :
                centralite_inter = nx.betweenness_centrality(G)
                centralite_prox = nx.closeness_centrality(G)
                centralite_inter_sorted=dict(sorted(centralite_inter.items(), key=lambda item: item[1], reverse = True))
                centralite_prox_sorted=dict(sorted(centralite_prox.items(), key=lambda item: item[1], reverse = True))
                
                title_obj = plt.title("size-->betweenness centrality \n color-->closeness centrality")
                plt.setp(title_obj, color='b') 
                
                #fig = plt.figure()
                #gs  = gridspec.GridSpec(1, 2, width_ratios=[6, 0.5])
                #ax0 = plt.subplot(gs[0])
                #ax1 = plt.subplot(gs[1])
                plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99 , top=0.9, wspace=0, hspace=0)
                
                
                cent = np.fromiter(centralite_prox.values(), float)
                normalize = mcolors.Normalize(vmin=cent.min(), vmax=cent.max())
                colormap = cm.summer
                scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
                scalarmappaple.set_array(centralite_prox)
                plt.colorbar(scalarmappaple,shrink=0.5)
                
                nx.draw(G,with_labels=True,node_size=[v * 500 + 200 for v in centralite_inter.values()], node_color=[v for v in centralite_prox.values()], cmap=colormap, linewidths=1)
                ax = plt.gca()
                ax.collections[0].set_edgecolor("#555")
                plt.savefig('static/assets/images/graphe_inter_prox.png')
                plt.close()
                
                N_inter=dict(list(centralite_inter_sorted.items())[:N])
                N_prox=dict(list(centralite_prox_sorted.items())[:N])
                return render_template('graphe.html', results=results, leng=leng, flash_message="23", D=N_inter, E=N_prox)
            elif request.form.get('check-1') :
                degre_centralite = nx.degree_centrality(G)
                degre_centralite_sorted=dict(sorted(degre_centralite.items(), key=lambda item: item[1],  reverse = True))
                fig = plt.figure()
                ax0 = fig.add_subplot()
                ax1 = fig.add_subplot()
                plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99 , top=0.99, wspace=0, hspace=0)
                nx.draw(G, ax=ax0,with_labels=True,node_size=[v * 500 + 200 for v in degre_centralite.values()])
                ax1.axis('off')
                ax1.text(0,0,"size-->degree centrality",fontdict=None,color="blue")
                plt.savefig('static/assets/images/graphe_degre.png')
                plt.close()
                
                N_degre=dict(list(degre_centralite_sorted.items())[:N])
                return render_template('graphe.html', results=results, leng=leng, flash_message="1", D=N_degre)
            elif request.form.get('check-2') :
                centralite_inter = nx.betweenness_centrality(G)
                centralite_inter_sorted=dict(sorted(centralite_inter.items(), key=lambda item: item[1], reverse = True))
                fig = plt.figure()
                ax0 = fig.add_subplot()
                ax1 = fig.add_subplot()
                plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99 , top=0.99, wspace=0, hspace=0)
                nx.draw(G, ax=ax0, with_labels=True, node_size=[v * 500 + 200 for v in centralite_inter.values()])
                ax1.axis('off')
                ax1.text(0,0,"size-->betweenness centrality",fontdict=None,color="blue")
                plt.savefig('static/assets/images/graphe_inter.png')
                plt.close()
                
                N_inter=dict(list(centralite_inter_sorted.items())[:N])
                return render_template('graphe.html', results=results, leng=leng, flash_message="2", D=N_inter)
            elif request.form.get('check-3') :
                centralite_prox = nx.closeness_centrality(G)
                centralite_prox_sorted=dict(sorted(centralite_prox.items(), key=lambda item: item[1], reverse = True))
                fig = plt.figure()
                ax0 = fig.add_subplot()
                ax1 = fig.add_subplot()
                plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99 , top=0.99, wspace=0, hspace=0)
                nx.draw(G, ax=ax0,with_labels=True,node_size=[v * 500 + 200 for v in centralite_prox.values()])
                ax1.axis('off')
                ax1.text(0,0,"size-->closeness centrality",fontdict=None,color="blue")
                plt.savefig('static/assets/images/graphe_prox.png')
                plt.close()
                print(centralite_prox)
                
                N_prox=dict(list(centralite_prox_sorted.items())[:N])
                return render_template('graphe.html', results=results, leng=leng, flash_message="3", D=N_prox)
            else :
                fig = plt.figure()
                ax0 = fig.add_subplot()
                ax1 = fig.add_subplot()
                plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99 , top=0.99, wspace=0, hspace=0)
                nx.draw(G, ax=ax0,with_labels=True,node_size=1000,edge_color='g')
                ax1.axis('off')
                ax1.text(0,0,"graph",fontdict=None,color="blue")
                plt.savefig('static/assets/images/graphe.png')
                plt.close()
                return render_template('graphe.html',results=results,leng=leng,flash_message="0")
 
        
        return render_template('graphe.html',results=results,leng=leng)       
        
        


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    