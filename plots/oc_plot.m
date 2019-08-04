#! usr/bin/ -qf

printf("Started\n"); %begin the program (octave does not accept begin with a function)

function save_pdf (vector1, vector2)  %Function that saves the graphic in a PDF archive
  graphic = plot( vector1, vector2, "marker", ".", "color", "b", "markersize", 15, "linestyle", "none" );  %Create a graphic with x axix == vector 1, and a y axis == vector 2. That graphic contains blue dot markers of size == 15. Don't have lines.

  saveas(graphic, "graphic.pdf"); #save the graphic in PDF
  endfunction

function plot_csv (archive)  #Function that creat a animated graphic of a csv file
  
  a = csvread(archive);
  len = length( a );    #length of a
  maximum = max( a( 1:len, 5 ) );   #max valor of csv file
  minimum = min( a( 1:len, 5 ) );   #min valor of csv file
  
  figure;

  week_std = 0;   #start the standard deviation for future use
  arithmetic_mean = [];   #start the vector with arithmetic means for every week in csv file
  standard_deviation = [];  #same as arithmetic_mean, but for standard deviation
  max_std = 0;  #max standard deviation valor
  min_std = 0;  #min standard deviation valor
    
  for i=7:7:len   #i cont every seven until the last element of csv archive
    week = [a(i-6, 5), a(i-5, 5), a(i-4, 5), a(i-3, 5), a(i-2, 5), a(i-1, 5), a(i, 5)];   #receives a vector equivalent of days of the week
    week_mean = mean( week );  #get the arithmetic mean of week
    week_std = std( week );  #get the standard deviation of week
    
    arithmetic_mean = [arithmetic_mean, week_mean];   #increment the media of week
    standard_deviation = [standard_deviation, week_std]; #increment the standard deviation of week
    
    if (week_std >= max_std)  #Get the bisggest valor of week_std
      max_std = week_std;
    endif
    
    if (week_std <= min_std)  #Get the smallest valor of week_std
      min_std = week_std;
    endif
  endfor

  for i=1:2:length(arithmetic_mean)   #i goes from 1, to the last element of arithmetic_mean by 2 steps
    axis([minimum maximum min_std max_std])  #creates the limit of the graphic
    
    plot( arithmetic_mean(i) , standard_deviation(i), "marker", ".", "color", "b", "markersize", 15 );    #creates the first point
    plot( arithmetic_mean(i+1) , standard_deviation(i+1), "marker", ".", "color", "b", "markersize", 15 );  #creates the second point (I used this because of the delay that is caused)
    
    xlabel ("Arithmetic mean");   #name of x axis
    ylabel ("Standard deviation");  #name of y axix
    title ("Graphic of media and Standard deviation for weeks");   #title
    
    hold on;    #keep the graphic on screen
    pause(0.000000001);   #create a delay (in this case, accelerate)
  endfor  
  
endfunction

arg_list = argv ();   #receive the arguments in command line
arg_list(2,:) = {" "};  #transform in string
arg_list = [arg_list{1:length(arg_list)-1}];  #set order 

plot_csv( arg_list );   