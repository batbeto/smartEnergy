#! usr/bin/ -qf

printf("Started\n");

function plot_kmeans(  )
    db = csvread( "2018-05-12.csv" );
    
    C1 = [db( 1:end, 6 )];
    C2 = [db( 1:end, 4 )];
    data = [C1, C2];

    ## Perform clustering
    [idx, centers] = kmeans(data, 5);

    ## Plot the result
    figure;
    plot (data (idx==1, 1), data (idx==1, 2), 'ro', "markerfacecolor", "r");
    hold on;
    plot (data (idx==2, 1), data (idx==2, 2), 'bo', "markerfacecolor", "b");
    hold on;
    plot (data (idx==3, 1), data (idx==3, 2), 'go', "markerfacecolor", "g");
    hold on;
    plot (data (idx==4, 1), data (idx==4, 2), 'mo', "markerfacecolor", "m");
    hold on;
    plot (data (idx==5, 1), data (idx==5, 2), 'co', "markerfacecolor", "c");

    plot (centers (:, 1), centers (:, 2), 'kv', 'markersize', 10, "markerfacecolor", "k");
    hold off;
    
endfunction 
plot_kmeans(  );