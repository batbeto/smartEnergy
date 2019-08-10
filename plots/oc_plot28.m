#! user/bin/ -qf

printf("Started\n");

#{
function precision_color( percent )
    switch percent
endfunction
#}
function csv_plot( file )
    db = csvread( file );
    
    arithimetic_mean_28 = db( 1:end, 1 );
    alert = db( 1:end, 1 ) + 1.5*db( 1:end, 3 );
    alert_down = db( 1:end, 1 ) - 1.5*db( 1:end, 3 );
    arithimetic_mean_day = db( 1:end, 4 );

    for i=2:1:length( db )
        
        axis([ i-30 i+10 min(alert_down)-100 max(alert) + 50 ])

        
        if arithimetic_mean_day(i) == -1
            plot( [i-1, i], [arithimetic_mean_day(i-1), arithimetic_mean_day(i)], "color", "k", "linestyle", "none" );
        elseif arithimetic_mean_day(i-1) == -1
            plot( i, arithimetic_mean_day(i), "color", "b", "linewidth", 2 );
        else
            plot( [i-1, i], [arithimetic_mean_day(i-1), arithimetic_mean_day(i)],"bo-","color", "b", "linewidth", 2, "markersize", 2.5 );
        endif
        plot( [i-1, i], [arithimetic_mean_28(i-1), arithimetic_mean_28(i)], "color", "r", "linewidth", 2 );

        plot( [i-1, i], [alert(i-1), alert(i)], "color", "r", "linewidth", 1 );
        plot( [i-1, i], [alert_down(i-1), alert_down(i)], "color", "r", "linewidth", 1 );


        hold on;

        pause(0.02);
    endfor

    figure(1);
    hold on;

    #pause(30);

    file_name = cstrcat( file, ".pdf" );
    print ( 1, file_name );

endfunction

arg_list = argv ();   #receive the arguments in command line
archive = strjoin( arg_list( 1, 1 ) );

csv_plot( archive );