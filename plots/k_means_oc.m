#! usr/bin/ -qf

pkg load statistics

printf("Started\n");

function color = color_to_plot ( num )
    if num == 1
        color = [0.066, 0.105, 0.690];
    elseif num == 2
        color = [0.945, 0.917, 0.294];
    elseif num == 3
        color = [0.827, 0, 0.513];
    elseif num == 4
        color = [1, 0.545, 0.184];
    elseif num == 5
        color = [0.588, 0, 0.619];
    elseif num == 6
        color = [1, 0.325, 0.282];
    elseif num == 7
        color = [1, 0.741, 0.164];
    else
        color = [0.976, 0, 0.392];
    endif
endfunction

function plot_kmeans( file, num )
    db = csvread( file );
    k = str2num(num);
    
    maxM_h = max( db( 1:end, 1 ) );
    minM_h = min( db( 1:end, 1 ) );
    maxStd_h = max( db( 1:end, 3 ) );
    minStd_h = min( db( 1:end, 3 ) );

    C1 = [];
    C2 = [];
    for i=1:length(db)
        if db(i, 4) != -1
            C1 = [C1; db( i, 4 )];
            C2 = [C2; db( i, 6 )];
        endif
    endfor
    data = [C1, C2];

    ## Perform clustering
    [idx, centers] = kmeans(data, k);

    ## Plot the result
    ";K-means to data analisys;";
    figure;

    for i=1:k
        color = color_to_plot( i );
        plot (data (idx==i, 1), data (idx==i, 2), 'd', "color", color, "markerfacecolor", color);
        hold on;
    endfor

    plot (centers (:, 1), centers (:, 2), 'kv', 'markersize', 10, "markerfacecolor", "k");
    hold on;
    #plot ( [minM_h, minM_h, maxM_h, maxM_h, minM_h], [minStd_h, maxStd_h, maxStd_h, minStd_h, minStd_h], "linewidth", 2, "color", "r" );
    rectangle('position', [minM_h, minStd_h, maxM_h - minM_h, maxStd_h - minStd_h], "facecolor", [0.905, 0.960, 0.980], "edgecolor", "b", "linewidth", 1);
    hold on;

    pause(10);
    hold off;
    
endfunction

arg_list = argv ();   #receive the arguments in command line
archive = strjoin( arg_list( 1, 1 ) );
num = strjoin( arg_list( 2, 1 ) );

plot_kmeans( archive, num );