import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Générer des points aléatoires
np.random.seed(42)
points = np.random.rand(20, 2) * 10

# Créer le diagramme de Voronoï
vor = Voronoi(points)

# Créer la figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Premier graphique : Diagramme de Voronoï simple
voronoi_plot_2d(vor, ax=ax1, show_vertices=False, line_colors='orange', 
                line_width=2, point_size=10)
ax1.set_xlim([-1, 11])
ax1.set_ylim([-1, 11])
ax1.set_title('Diagramme de Voronoï', fontsize=14, fontweight='bold')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.grid(True, alpha=0.3)

# Deuxième graphique : Version colorée avec remplissage
voronoi_plot_2d(vor, ax=ax2, show_vertices=False, line_colors='black', 
                line_width=1.5, point_size=10)

# Colorier les régions
for region in vor.regions:
    if not -1 in region and len(region) > 0:
        polygon = [vor.vertices[i] for i in region]
        ax2.fill(*zip(*polygon), alpha=0.4, edgecolor='black', linewidth=1.5)

ax2.set_xlim([-1, 11])
ax2.set_ylim([-1, 11])
ax2.set_title('Diagramme de Voronoï (régions colorées)', fontsize=14, fontweight='bold')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/voronoi_diagram.png', dpi=300, bbox_inches='tight')
print("✓ Diagramme de Voronoï créé avec succès!")
print(f"✓ Nombre de points: {len(points)}")
print(f"✓ Nombre de régions: {len(vor.regions)}")
print("✓ Image sauvegardée: voronoi_diagram.png")

plt.show()
