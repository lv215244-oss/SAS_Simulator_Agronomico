CROPS = {
    'Frijol negro': dict(cap_temporal=2000, cap_riego=2800, base_temp=8, opt_temp=24, max_temp=34, season_days=105, kg_biomass_to_yield=0.34, root_depth=0.80, kc=0.90, n_demand=115, harvest_index=0.34),
    'Frijol pinto': dict(cap_temporal=2000, cap_riego=2800, base_temp=8, opt_temp=24, max_temp=34, season_days=105, kg_biomass_to_yield=0.34, root_depth=0.80, kc=0.90, n_demand=115, harvest_index=0.34),
    'Maíz': dict(cap_temporal=7500, cap_riego=12000, base_temp=10, opt_temp=26, max_temp=40, season_days=125, kg_biomass_to_yield=0.48, root_depth=1.50, kc=1.05, n_demand=180, harvest_index=0.48),
    'Calabaza': dict(cap_temporal=900, cap_riego=1800, base_temp=8, opt_temp=25, max_temp=38, season_days=120, kg_biomass_to_yield=0.35, root_depth=1.00, kc=0.85, n_demand=100, harvest_index=0.35),
    'Trigo': dict(cap_temporal=4500, cap_riego=7000, base_temp=0, opt_temp=18, max_temp=35, season_days=145, kg_biomass_to_yield=0.45, root_depth=1.20, kc=1.00, n_demand=160, harvest_index=0.45),
    'Cebada': dict(cap_temporal=4500, cap_riego=6500, base_temp=0, opt_temp=18, max_temp=35, season_days=135, kg_biomass_to_yield=0.45, root_depth=1.10, kc=1.00, n_demand=150, harvest_index=0.45),
}
SOILS = {
    'Franco': dict(theta_fc=0.28, theta_wp=0.13, depth=1.20, bulk_density=1.25, om=1.5, pH=7.5),
    'Franco arcilloso': dict(theta_fc=0.32, theta_wp=0.16, depth=1.20, bulk_density=1.30, om=1.8, pH=7.7),
    'Arcilloso': dict(theta_fc=0.36, theta_wp=0.20, depth=1.20, bulk_density=1.35, om=2.0, pH=7.8),
    'Arenoso franco': dict(theta_fc=0.22, theta_wp=0.10, depth=1.00, bulk_density=1.45, om=1.2, pH=7.4),
}
