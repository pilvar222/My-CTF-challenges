require 'asciidoctor'
require 'base64'

class Asciidoc2htmlController < ApplicationController
    def index
        if(params.has_key?(:input))
            begin
                input = params[:input]
                input = Base64.decode64(input).downcase.sub("+","").sub("<","").sub(">","").sub("pass","X") # we're safe now!
                output = Asciidoctor.convert(input, safe: :safe).html_safe
            rescue
                output = "Invalid input"
            end
        else
            output = ""
        end
        render :index, locals: { output: output }
    end
end
