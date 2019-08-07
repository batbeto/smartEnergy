#! user/bin/ -qf

printf("Started\n");

function csv_plot( file )
    db = csvread( file );
    
    arithimetic_mean_28 = db( 1:end, 1 );
    arithimetic_mean_day = db( 1:end, 2 );

    for i=2:1:length( db )
        #axis([ 0 length( db ) 0 max(arithimetic_mean_day) ])

        plot( [i-1, i], [arithimetic_mean_day(i-1), arithimetic_mean_day(i)], "color", "b", "linewidth", 2 );
        plot( [i-1, i], [arithimetic_mean_28(i-1), arithimetic_mean_28(i)], "color", "r", "linewidth", 2 );
        hold on;

        pause(0.000000001);
    endfor

endfunction

arg_list = argv ();   #receive the arguments in command line
archive = strjoin( arg_list( 1, 1 ) );

csv_plot( archive );