require 'cosmos'
require 'cosmos/tools/tlm_viewer/widgets/value_widget'

module Cosmos

  class TimesinceupdateWidget < ValueWidget
	
    def initialize (parent_layout, target_name, packet_name, item_name, value_type = :CONVERTED, characters = 12)
	  
      super(parent_layout, target_name, packet_name, item_name, value_type, characters)
      
	  @numRecieved = tlm(target_name, packet_name, "RECEIVED_COUNT")
	  @update_time=Time.now.to_i
	  @formatted_data = "NA"
	  @prev_val=tlm(target_name, packet_name, item_name)
	  @known = false
	  parent_layout.addWidget(self) if parent_layout
    end

    def value= (data)
	  newNumRecieved=tlm(target_name, packet_name,"RECEIVED_COUNT")
	  if newNumRecieved-@numRecieved > 0 
		delta=data.to_i - @prev_val.to_i
		@numRecieved=newNumRecieved
		if delta > 0
			@known = true
			@update_time=tlm(target_name, packet_name, "RECEIVED_TIMESECONDS")
		end
		@prev_val=tlm(target_name, packet_name, item_name)
	  end
	  if @known
		time=Time.now.to_i
		hours=((time-@update_time+5)/3600).to_i
		minutes=((time-@update_time-3600*hours+5)/60).to_i
		seconds = time-@update_time-minutes*60-hours*3600+5
		@formatted_data="#{hours}:#{minutes}:#{seconds.to_i}"
	  end
      super(@formatted_data)
	  
    end

  end

end # module Cosmos