#! usr/bin/ -qf

printf("Started\n"); %begin the program (octave does not accept begin with a function)

function field = switch_field( choice )
  
  switch( choice )
    case "FPA"
      field = 2;
    case "FPB"
      field = 3;
    case "FPC"
      field = 4;
    case "P1"
      field = 5;
    case "P2"
      field = 6;
    case "P3"
      field = 7;
    case "Q1"
      field = 8;
    case "Q2"
      field = 9;
    case "Q3"
      field = 10;
    otherwise
      field = 5;
  endswitch;

endfunction

function list = get_day_mean( file )
  list = [];
  week_day = [];
  last_day = 8;
  cont = 0;
  for i=1:length( file )
    wd = file(i, 1);
    if last_day == wd || last_day == 8
      switch (length(week_day))
      case 0
        week_day = file(i, 1:end);
        cont += 1;
      otherwise
        week_day = [ week_day(1), week_day(2:end) + file( i, 2:end )];
        cont += 1;
      endswitch
    else
      week_day = [week_day(1), week_day( 2:end ) / cont];
      list = [list; week_day ];
      week_day = file( i, 1:end );
      cont = 1;
    endif
    last_day = wd;
  endfor
  week_day = [week_day(1), week_day( 2:end ) / cont];
  list = [list; week_day ];
endfunction

function list = get_week_mean( vector )
  last_day = 8;
  list = [];
  week = [];
  cont = 0;
  for i=1:length( vector )
    wd = vector(i, 1);
    if wd > last_day || last_day == 8
      switch (length(week))
        case 0
          week = vector(i, 1:end);
          cont += 1;
        otherwise
          week = [ week(1), week( 2:end ) + vector( i, 2:end )];
          cont += 1;
      endswitch
    else
      week = [ week(1), week( 2:end ) / cont];
      list = [list; week];
      cont = 1;
      week = vector(i, 1:end);
    endif
    last_day = wd;
  endfor
  week = [ week(1), week( 2:end ) / cont];
  list = [list; week];
endfunction

function list = get_week_sd( vector )
  last_day = 8;
  list = [];
  week_sd = [];
  cont = 0;
  for i=1:length( vector )
    wd = vector( i, 1 );
    if wd > last_day || last_day == 8
      switch length( week_sd ) 
        case 0
          week_sd = vector(i, 1:end);
        otherwise
          week_sd = [week_sd; vector(i, 1:end)];
      endswitch
    else
      list = [list; week_sd(1, 1), std( week_sd(1:end, 2) ), std( week_sd(1:end, 3) ), std( week_sd(1:end, 4) ), std( week_sd(1:end, 5) ), std( week_sd(1:end, 6) ), std( week_sd(1:end, 7) ), std( week_sd(1:end, 8) ), std( week_sd(1:end, 9) ), std( week_sd(1:end, 10) )];
      week_sd = vector( i, 1:end );
    endif
    last_day = wd;
  endfor
  list = [list; week_sd(1, 1), std( week_sd(1:end, 2) ), std( week_sd(1:end, 3) ), std( week_sd(1:end, 4) ), std( week_sd(1:end, 5) ), std( week_sd(1:end, 6) ), std( week_sd(1:end, 7) ), std( week_sd(1:end, 8) ), std( week_sd(1:end, 9) ), std( week_sd(1:end, 10) )];
endfunction

function plot_csv (archive, field)  #Function that creat a animated graphic of a csv file
  choice = switch_field( field );

  file = csvread( archive );
  weekdays = get_day_mean( file );

  week_std = 0;   #start the standard deviation for future use
  format "bank";
  arithmetic_mean = get_week_mean( weekdays );   #start the vector with arithmetic means for every week in csv file
  standard_deviation = get_week_sd( weekdays );  #same as arithmetic_mean, but for standard deviation

  maximum = max( arithmetic_mean( 1:end, choice ) );   #max valor of csv file
  minimum = min( arithmetic_mean( 1:end, choice ) );   #min valor of csv file
  
  max_std = max( standard_deviation( 1:end, choice ) );;  #max standard deviation valor
  min_std = min( standard_deviation( 1:end, choice ) );  #min standard deviation valor

  for i=1:length(arithmetic_mean)   #i goes from 1, to the last element of arithmetic_mean by 2 steps
    axis([minimum maximum min_std max_std])  #creates the limit of the graphic
    
    plot( arithmetic_mean(i, choice) , standard_deviation(i, choice), "ob", "markerfacecolor", "b", "markersize", 5 );    #creates the first point
    
    xlabel ("Arithmetic mean");   #name of x axis
    ylabel ("Standard deviation");  #name of y axix
    title ("Graphic of media and Standard deviation for weeks");   #title
    
    hold on;    #keep the graphic on screen
    pause(1);   #create a delay (in this case, accelerate)
  endfor
  figure(1);
  hold on;

  pause(10);

  #file_name = cstrcat( archive, field, ".pdf" );
  #print ( 1, file_name );
  
endfunction

arg_list = argv ();   #receive the arguments in command line
archive = strjoin( arg_list( 1, 1 ) );
field = strjoin( arg_list( 2, 1 ) );

plot_csv( archive, field );