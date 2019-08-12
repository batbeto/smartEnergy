#! user/bin/ -qf

printf("Started\n");

function color = precision_color( percent )
    if percent <= 25.0
        color = [1, 0, 0.101];
    elseif percent <= 50.0
        color = [1, 0.6, 0.129];
    elseif percent <= 75.0
        color = [0.886, 0.933, 0.207];
    elseif percent <= 100.0
        color =  [0.282, 0.772, 0.207];
    else
        color = "w";
    endif
endfunction

function csv_plot( file )
    db = csvread( file );
    
    arithimetic_mean_28 = db( 1:end, 1 );
    alert = db( 1:end, 1 ) + 1.5*db( 1:end, 3 );
    alert_down = db( 1:end, 1 ) - 1.5*db( 1:end, 3 );
    arithimetic_mean_day = db( 1:end, 4 );
    precision = db( 1:end, 5 );

    for i=2:1:length( db )
        
        axis([ i-30 i+10 min(alert_down)-100 max(alert) + 50 ]);
        pbaspect([2 1 1]);


        color = precision_color( precision(i) );

        if arithimetic_mean_day(i) == -1
            plot( [i-1, i], [arithimetic_mean_day(i-1), arithimetic_mean_day(i)], "color", "k", "linestyle", "none" );
        elseif arithimetic_mean_day(i-1) == -1
            plot( i, arithimetic_mean_day(i), "color", "b", "linewidth", 2 );
        else
            plot( [i-1, i], [arithimetic_mean_day(i-1), arithimetic_mean_day(i)],"bo-", "color", [0, 0.258, 0.615], "linewidth", 2, "markersize", 2.5, "markerfacecolor", color, "markeredgecolor", color );
        endif


        #set(gca,'color',[0.222, 0.214, 0.214])
        plot( [i-1, i], [arithimetic_mean_28(i-1), arithimetic_mean_28(i)], "color", [1, 0, 0], "linewidth", 2 );

        plot( [i-1, i], [alert(i-1), alert(i)], "color", [1, 0.337, 0.439], "linewidth", 1 );
        plot( [i-1, i], [alert_down(i-1), alert_down(i)], "color", [1, 0.337, 0.439], "linewidth", 1 );


        hold on;

        pause(0.02);
    endfor

    figure(1);
    axis([0 i+10 min( alert_down )-100 max( alert )+50 ]);
    pbaspect([3 1 1]);
    #set(gca,'color',[0.222, 0.214, 0.214]);
    hold on;

    pause(10);

    #file_name = cstrcat( file, ".pdf" );
    #print ( 1, file_name );

endfunction

arg_list = argv ();   #receive the arguments in command line
archive = strjoin( arg_list( 1, 1 ) );

csv_plot( archive );