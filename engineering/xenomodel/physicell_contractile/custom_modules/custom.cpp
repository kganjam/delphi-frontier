/*
 Contractile-construct test module for PhysiCell 1.14.2 (BSD-3-Clause, Macklin et al.).
 Author: claude-xenomodel harness, 2026-11-01. Not part of upstream PhysiCell.

 What it does (all parameters read from environment variables, see xm_param):
   XM_MODE   springs | native
     springs: cells are joined at setup by linear springs to every neighbour within 1.1*r0;
              the spring force on i from j is k*(|d| - L_ij(t)) * d/|d|, d = x_j - x_i,
              with prescribed rest length L_ij(t) = r0*(1 - eps*(1 - cos(w t - dir*q*xbar_ij))/2),
              xbar_ij the reference-configuration midpoint x. PhysiCell repulsion/adhesion are
              set to zero in this mode, so the springs are the only forces.
     native : no custom springs; PhysiCell's own repulsion/adhesion potentials act, and the
              actuation is a prescribed cyclic cell radius
              R_i(t) = R0*(1 - eps*(1 - cos(w t - dir*q*x_i0))/2).
   Velocity: PhysiCell mechanics are overdamped (velocity = summed force, unit mobility).
     After all forces are summed, the x-velocity is divided by XM_XIP if >= 0 and by XM_XIM if < 0
     (direction-dependent substrate drag). XM_XIP = XM_XIM = 1 recovers stock PhysiCell mobility.
   XM_GEOM   pair  : two cells on the x axis
             strip : centred hexagonal strip, XM_NX cells in even rows, XM_NX-1 in odd rows,
                     XM_NY rows; mirror-symmetric about x = 0 by construction.
 Contraction is this project's modelling choice; the CDO sources report ciliary locomotion.
*/

#include "./custom.h"
#include <cstdlib>
#include <cmath>
#include <fstream>

static double xm_param( const char* name , double def )
{
	const char* s = std::getenv( name );
	return s ? std::atof( s ) : def;
}
static std::string xm_str( const char* name , const char* def )
{
	const char* s = std::getenv( name );
	return s ? std::string( s ) : std::string( def );
}

struct XMSpring { int a; int b; double xbar; };
static std::vector<XMSpring> xm_springs;
static std::vector<double> xm_x0;           // reference x by cell index
static std::vector<double> xm_force_x, xm_force_y;
static double xm_r0, xm_k, xm_eps, xm_q, xm_dir, xm_w, xm_xip, xm_xim, xm_R0;
static bool xm_native;

static double xm_rest_length( double t , double xbar )
{
	return xm_r0 * ( 1.0 - xm_eps * 0.5 * ( 1.0 - std::cos( xm_w * t - xm_dir * xm_q * xbar ) ) );
}

// Compute all spring forces once per mechanics step (called from cell 0's custom rule,
// which PhysiCell evaluates before any update_velocity). Pairwise antisymmetric by construction.
void xm_compute_spring_forces( double t )
{
	int n = (*all_cells).size();
	xm_force_x.assign( n , 0.0 ); xm_force_y.assign( n , 0.0 );
	for( const auto& s : xm_springs )
	{
		Cell* A = (*all_cells)[s.a]; Cell* B = (*all_cells)[s.b];
		double dx = B->position[0] - A->position[0];
		double dy = B->position[1] - A->position[1];
		double d = std::sqrt( dx*dx + dy*dy );
		if( d <= 0 ) continue;
		double f = xm_k * ( d - xm_rest_length( t , s.xbar ) ) / d;
		xm_force_x[s.a] += f*dx; xm_force_y[s.a] += f*dy;
		xm_force_x[s.b] -= f*dx; xm_force_y[s.b] -= f*dy;
	}
}

void xm_custom_rule( Cell* pCell, Phenotype& phenotype, double dt )
{
	// cell 0 computes every spring force for this mechanics step; the custom-rule loop
	// finishes (OpenMP barrier) before the update_velocity loop starts
	if( !xm_native && pCell->index == 0 ) { xm_compute_spring_forces( PhysiCell_globals.current_time ); }
	if( xm_native )
	{
		double R = xm_R0 * ( 1.0 - xm_eps * 0.5 * ( 1.0 - std::cos( xm_w * PhysiCell_globals.current_time - xm_dir * xm_q * xm_x0[pCell->index] ) ) );
		pCell->set_total_volume( 4.0/3.0 * M_PI * R*R*R );
	}
}

void xm_update_velocity( Cell* pCell, Phenotype& phenotype, double dt )
{
	standard_update_cell_velocity( pCell , phenotype , dt );
	if( !xm_native )
	{
		pCell->velocity[0] += xm_force_x[pCell->index];
		pCell->velocity[1] += xm_force_y[pCell->index];
	}
	double vx = pCell->velocity[0];
	pCell->velocity[0] = ( vx >= 0.0 ) ? vx / xm_xip : vx / xm_xim;
}

void create_cell_types( void )
{
	SeedRandom( (int) xm_param( "XM_SEED" , 0 ) );
	initialize_default_cell_definition();
	cell_defaults.phenotype.secretion.sync_to_microenvironment( &microenvironment );
	cell_defaults.functions.volume_update_function = standard_volume_update_function;
	cell_defaults.functions.update_velocity = standard_update_cell_velocity;
	cell_defaults.functions.update_migration_bias = NULL;
	cell_defaults.functions.update_phenotype = NULL;
	cell_defaults.functions.custom_cell_rule = NULL;
	cell_defaults.functions.contact_function = NULL;
	cell_defaults.functions.add_cell_basement_membrane_interactions = NULL;
	cell_defaults.functions.calculate_distance_to_membrane = NULL;
	initialize_cell_definitions_from_pugixml();
	build_cell_definitions_maps();
	setup_signal_behavior_dictionaries();
	setup_cell_rules();

	xm_native = ( xm_str( "XM_MODE" , "springs" ) == "native" );
	xm_r0 = xm_param( "XM_R0" , 16.0 );
	xm_k = xm_param( "XM_K" , 0.5 );
	xm_eps = xm_param( "XM_EPS" , 0.1 );
	double lambda = xm_param( "XM_LAMBDA" , 0.0 ); // wavelength in micron; 0 = standing (no phase gradient)
	xm_q = ( lambda > 0 ) ? 2.0*M_PI/lambda : 0.0;
	xm_dir = xm_param( "XM_DIR" , 1.0 );
	xm_w = 2.0*M_PI / xm_param( "XM_PERIOD" , 30.0 );
	xm_xip = xm_param( "XM_XIP" , 1.0 );
	xm_xim = xm_param( "XM_XIM" , 1.0 );

	Cell_Definition* pCD = cell_definitions_by_index[0];
	// no proliferation, no death, no motility: mechanics only
	for( auto& v : pCD->phenotype.cycle.data.transition_rates ) for( auto& r : v ) r = 0.0;
	for( auto& r : pCD->phenotype.death.rates ) r = 0.0;
	pCD->phenotype.motility.is_motile = false;
	pCD->functions.custom_cell_rule = xm_custom_rule;
	pCD->functions.update_velocity = xm_update_velocity;
	pCD->functions.update_phenotype = NULL;
	if( xm_native )
	{
		pCD->functions.volume_update_function = NULL; // radius is prescribed by the actuation
	}
	else
	{
		pCD->phenotype.mechanics.cell_cell_adhesion_strength = 0.0;
		pCD->phenotype.mechanics.cell_cell_repulsion_strength = 0.0;
		pCD->functions.volume_update_function = NULL;
	}
	display_cell_definitions( std::cout );
}

void setup_microenvironment( void )
{
	initialize_microenvironment();
}

void setup_tissue( void )
{
	Cell_Definition* pCD = cell_definitions_by_index[0];
	std::string geom = xm_str( "XM_GEOM" , "pair" );
	std::vector<std::vector<double>> pos;
	double r0 = xm_r0;
	if( geom == "pair" )
	{
		pos.push_back( { -0.5*r0 , 0 , 0 } );
		pos.push_back( {  0.5*r0 , 0 , 0 } );
	}
	else
	{
		int nx = (int) xm_param( "XM_NX" , 10 );
		int ny = (int) xm_param( "XM_NY" , 3 );
		double h = r0 * std::sqrt( 3.0 ) / 2.0;
		for( int j=0; j < ny; j++ )
		{
			int n = ( j % 2 == 0 ) ? nx : nx - 1;
			for( int i=0; i < n; i++ )
				pos.push_back( { ( i - 0.5*(n-1) ) * r0 , ( j - 0.5*(ny-1) ) * h , 0 } );
		}
	}
	for( auto& p : pos )
	{
		Cell* pC = create_cell( *pCD );
		pC->assign_position( p );
		xm_x0.push_back( p[0] );
	}
	xm_R0 = (*all_cells)[0]->phenotype.geometry.radius;
	if( !xm_native )
	{
		for( int a=0; a < (int) pos.size(); a++ )
			for( int b=a+1; b < (int) pos.size(); b++ )
			{
				double dx = pos[b][0]-pos[a][0], dy = pos[b][1]-pos[a][1];
				if( std::sqrt( dx*dx+dy*dy ) < 1.1*r0 )
					xm_springs.push_back( { a , b , 0.5*(pos[a][0]+pos[b][0]) } );
			}
	}
	std::cout << "XM setup: cells=" << pos.size() << " springs=" << xm_springs.size()
	          << " native=" << xm_native << " R0=" << xm_R0 << std::endl;
}

std::vector<std::string> my_coloring_function( Cell* pCell )
{ return paint_by_number_cell_coloring( pCell ); }

void phenotype_function( Cell* pCell, Phenotype& phenotype, double dt ) { return; }
void custom_function( Cell* pCell, Phenotype& phenotype , double dt ) { return; }
void contact_function( Cell* pMe, Phenotype& phenoMe , Cell* pOther, Phenotype& phenoOther , double dt ) { return; }
