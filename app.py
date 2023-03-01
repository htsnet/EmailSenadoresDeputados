import streamlit as st
from time import sleep
import smtplib
from email.mime.text import MIMEText

# ver emojis em https://emojipedia.org/coin/

st.set_page_config(page_title='Enviar mensagens individuais a Deputados Federais e Senadores', 
                   page_icon=':envelope', layout='centered', initial_sidebar_state='expanded' )

#para esconder o menu do próprio streamlit 
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
# passa javascript e estilos
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    with st.sidebar:
        st.header('Informações sobre o uso')
        st.write('1 - Informe seu servidor SMTP, conta e senha. ')
        st.write('2 - Escreva seu texto (respeitosamente) para ser encaminhado a cada representante.')
        st.write('3 - Confira atentamente o texto antes de prosseguir.')
        st.write('4 - Escolha o grupo de destinatários da sua mensagem.')
        st.write('5 - Há um intervalo proposital de 5 segundos entre cada disparo.')
            
        st.header('Sobre')
        st.write('‼️ ⚠️ Projeto em versão preliminar.')
        st.write('A lista de emails foi obtida na data de 01/03/2023 através do site https://www.vemprarua.net/.')
        st.write('Nem todos os representantes do povo fornecem seu endereço de e-mail para contato direto.')
        st.write('A responsabilidade pelo conteúdo da mensagem é exclusivamente sua.')
        st.write('Automaticamente será inserido no início de cada texto a frase: "Prezado Deputado Federal" ou "Prezado Senado".')
        st.write('Nenhuma informação é armazenada no servidor. A cada uso você precisará informar novamente os dados de sua conta.')
        st.write('Os detalhes e o código fonte sobre este projeto podem ser encontrados em https://github.com/htsnet/EmailSenadoresDeputados')
        
        st.header('Detalhe técnico')
        st.write('Se você usa um serviço de email com autenticação em 2 etapas será preciso gerar uma senha exclusiva para este disparo. Para o Gmail, siga este link: https://myaccount.google.com/apppasswords')
    
    # lista obtida nas páginas https://www.vemprarua.net/camara/br/# e https://www.vemprarua.net/senado/br/, na opção de exportar a lista de emaisl com separadores por vírgula
    # basta copiar todo o conteúdo e colar na variável respectiva
    senadores = """, sen.alessandrovieira@senado.leg.br, sen.anapaulalobato@senado.leg.br, sen.angelocoronel@senado.leg.br, , sen.augustabrito@senado.leg.br, , sen.carlosportinho@senado.leg.br, sen.carlosviana@senado.leg.br, sen.chicorodrigues@senado.leg.br, sen.cidgomes@senado.leg.br, sen.cironogueira@senado.leg.br, , sen.confuciomoura@senado.leg.br, , sen.daniellaribeiro@senado.leg.br, sen.davialcolumbre@senado.leg.br, , , sen.eduardobraga@senado.leg.br, sen.eduardogirao@senado.leg.br, sen.eduardogomes@senado.leg.br, , sen.elizianegama@senado.leg.br, sen.esperidiaoamin@senado.leg.br, sen.fabianocontarato@senado.leg.br, , sen.fernandofarias@senado.leg.br, sen.flavioarns@senado.leg.br, sen.flaviobolsonaro@senado.leg.br, , , sen.humbertocosta@senado.leg.br, sen.iraja@senado.leg.br, , sen.izalcilucas@senado.leg.br, sen.jaderbarbalho@senado.leg.br, , sen.jaqueswagner@senado.leg.br, Sen.JaymeCampos@senado.leg.br, sen.jorgekajuru@senado.leg.br, , , , sen.leilabarros@senado.leg.br, sen.lucasbarreto@senado.leg.br, sen.luiscarlosheinze@senado.leg.br, magno.malta@senador.leg.br, sen.maragabrilli@senado.leg.br, sen.marcelocastro@senado.leg.br, sen.marciobittar@senado.leg.br, sen.marcosdoval@senado.leg.br, sen.margarethbuzetti@senado.leg.br, sen.meciasdejesus@senado.leg.br, sen.nelsinhotrad@senado.leg.br, sen.omaraziz@senado.leg.br, sen.oriovistoguimaraes@senado.leg.br, sen.ottoalencar@senado.leg.br, sen.paulopaim@senado.leg.br, sen.pliniovalerio@senado.leg.br, , sen.randolferodrigues@senado.leg.br, sen.renancalheiros@senado.leg.br, sen.rodrigocunha@senado.leg.br, sen.rodrigopacheco@senado.leg.br, sen.rogeriocarvalho@senado.leg.br, , sen.romario@senado.leg.br, , sen.sergiopetecao@senado.leg.br, sen.sorayathronicke@senado.leg.br, sen.styvensonvalentim@senado.leg.br, , , sen.vanderlancardoso@senado.leg.br, sen.venezianovitaldorego@senado.leg.br, sen.wellingtonfagundes@senado.leg.br, sen.wevertonrocha@senado.leg.br, wilder.morais@senador.leg.br, sen.zenaidemaia@senado.leg.br, sen.zequinhamarinho@senado.leg.br"""
    # st.write(senadores)
    deputados_federais = """dep.abiliobrunini@camara.leg.br, dep.acaciofavacho@camara.leg.br, dep.adailfilho@camara.leg.br, dep.adilsonbarroso@camara.leg.br, dep.adolfoviana@camara.leg.br, dep.adrianaventura@camara.leg.br, dep.adrianodobaldy@camara.leg.br, dep.aecioneves@camara.leg.br, dep.afonsohamm@camara.leg.br, dep.afonsomotta@camara.leg.br, dep.aguinaldoribeiro@camara.leg.br, dep.airtonfaleiro@camara.leg.br, dep.ajalbuquerque@camara.leg.br, dep.albertofraga@camara.leg.br, dep.albertomourao@camara.leg.br, dep.albuquerque@camara.leg.br, dep.alceumoreira@camara.leg.br, dep.alencarsantana@camara.leg.br, dep.alexmanente@camara.leg.br, dep.alexsantana@camara.leg.br, dep.alexandreguimaraes@camara.leg.br, dep.alexandreleite@camara.leg.br, dep.alexandrelindenmeyer@camara.leg.br, dep.alfredinho@camara.leg.br, dep.alfredogaspar@camara.leg.br, dep.aliceportugal@camara.leg.br, dep.alielmachado@camara.leg.br, dep.altineucortes@camara.leg.br, dep.aluisiomendes@camara.leg.br, dep.amaliabarros@camara.leg.br, dep.amandagentil@camara.leg.br, dep.amaroneto@camara.leg.br, dep.amommandel@camara.leg.br, dep.anapaulaleao@camara.leg.br, dep.anapaulalima@camara.leg.br, dep.anapimentel@camara.leg.br, dep.andrefernandes@camara.leg.br, dep.andreferreira@camara.leg.br, dep.andrefigueiredo@camara.leg.br, dep.andrefufuca@camara.leg.br, dep.andrejanones@camara.leg.br, dep.andreiasiqueira@camara.leg.br, dep.antonialucia@camara.leg.br, dep.antonioandrade@camara.leg.br, dep.antoniobrito@camara.leg.br, dep.antoniocarlosrodrigues@camara.leg.br, dep.antoniodoido@camara.leg.br, dep.anyortiz@camara.leg.br, dep.arlindochinaglia@camara.leg.br, dep.arnaldojardim@camara.leg.br, dep.arthurlira@camara.leg.br, dep.arthuroliveiramaia@camara.leg.br, dep.atilalins@camara.leg.br, dep.augustocoutinho@camara.leg.br, dep.augustopupio@camara.leg.br, dep.aureoribeiro@camara.leg.br, dep.bacelar@camara.leg.br, dep.baleiarossi@camara.leg.br, dep.bandeirademello@camara.leg.br, dep.bebeto@camara.leg.br, dep.beneditadasilva@camara.leg.br, dep.benesleocadio@camara.leg.br, dep.betopereira@camara.leg.br, dep.betopreto@camara.leg.br, dep.betoricha@camara.leg.br, dep.biakicis@camara.leg.br, dep.bibonunes@camara.leg.br, dep.bohngass@camara.leg.br, dep.brunofarias@camara.leg.br, dep.brunoganem@camara.leg.br, dep.cabogilbertosilva@camara.leg.br, dep.junioamaral@camara.leg.br, dep.camilajara@camara.leg.br, dep.capitaoalbertoneto@camara.leg.br, dep.capitaoalden@camara.leg.br, dep.capitaoaugusto@camara.leg.br, dep.carlazambelli@camara.leg.br, dep.carloschiodini@camara.leg.br, dep.carlosgomes@camara.leg.br, dep.carloshenriquegaguim@camara.leg.br, dep.carlosjordy@camara.leg.br, dep.carlossampaio@camara.leg.br, dep.carlosveras@camara.leg.br, dep.carloszarattini@camara.leg.br, dep.caroldartora@camara.leg.br, dep.carolinedetoni@camara.leg.br, dep.castroneto@camara.leg.br, dep.celiaxakriaba@camara.leg.br, dep.celiosilveira@camara.leg.br, dep.celiostudart@camara.leg.br, dep.celsorussomanno@camara.leg.br, dep.celsosabino@camara.leg.br, dep.cezinhademadureira@camara.leg.br, dep.charlesfernandes@camara.leg.br, dep.chicoalencar@camara.leg.br, dep.chiquinhobrazao@camara.leg.br, dep.christonietto@camara.leg.br, dep.clarissatercio@camara.leg.br, dep.claudiocajado@camara.leg.br, dep.cleberverde@camara.leg.br, dep.clodoaldomagalhaes@camara.leg.br, dep.cobalchini@camara.leg.br, dep.coronelassis@camara.leg.br, dep.coronelchrisostomo@camara.leg.br, dep.coronelfernanda@camara.leg.br, dep.coronelmeira@camara.leg.br, dep.coroneltelhada@camara.leg.br, dep.coronelulysses@camara.leg.br, dep.covattifilho@camara.leg.br, dep.cristianelopes@camara.leg.br, dep.davitoria@camara.leg.br, dep.dagobertonogueira@camara.leg.br, dep.daianasantos@camara.leg.br, dep.dalbarreto@camara.leg.br, dep.damiaofeliciano@camara.leg.br, dep.dandara@camara.leg.br, dep.danicunha@camara.leg.br, dep.danielagrobom@camara.leg.br, dep.danielalmeida@camara.leg.br, dep.danielbarbosa@camara.leg.br, dep.danielfreitas@camara.leg.br, dep.danielsoranz@camara.leg.br, dep.danieltrzeciak@camara.leg.br, dep.danielareinehr@camara.leg.br, dep.daniloforte@camara.leg.br, dep.danrleidedeushinterholz@camara.leg.br, dep.davidsoares@camara.leg.br, dep.dayanydocapitao@camara.leg.br, dep.defensorsteliodener@camara.leg.br, dep.delegadaadrianaaccorsi@camara.leg.br, dep.delegadaione@camara.leg.br, dep.delegadakatarina@camara.leg.br, dep.delegadocaveira@camara.leg.br, dep.delegadodacunha@camara.leg.br, dep.delegadoedermauro@camara.leg.br, dep.delegadofabiocosta@camara.leg.br, dep.delegadomarcelofreitas@camara.leg.br, dep.delegadomatheuslaiola@camara.leg.br, dep.delegadopalumbo@camara.leg.br, dep.delegadopaulobilynskyj@camara.leg.br, dep.delegadoramagem@camara.leg.br, dep.deltandallagnol@camara.leg.br, dep.denisepessoa@camara.leg.br, dep.detinha@camara.leg.br, dep.diegoandrade@camara.leg.br, dep.diegocoronel@camara.leg.br, dep.diegogarcia@camara.leg.br, dep.dilceusperafico@camara.leg.br, dep.dilvandafaro@camara.leg.br, dep.dimasfabiano@camara.leg.br, dep.dimasgadelha@camara.leg.br, dep.domingosneto@camara.leg.br, dep.domingossavio@camara.leg.br, dep.dorinaldomalafaia@camara.leg.br, dep.drbenjamim@camara.leg.br, dep.dr.fernandomaximo@camara.leg.br, dep.dr.francisco@camara.leg.br, dep.dr.frederico@camara.leg.br, dep.dr.jaziel@camara.leg.br, dep.dr.luizovando@camara.leg.br, dep.dr.victorlinhalis@camara.leg.br, dep.dr.zachariascalil@camara.leg.br, dep.dra.alessandrahaber@camara.leg.br, dep.duarte@camara.leg.br, dep.dudaramos@camara.leg.br, dep.dudasalabert@camara.leg.br, dep.eduardobismarck@camara.leg.br, dep.eduardobolsonaro@camara.leg.br, dep.eduardodafonte@camara.leg.br, dep.eduardovelloso@camara.leg.br, dep.elcionebarbalho@camara.leg.br, dep.eliborges@camara.leg.br, dep.elmarnascimento@camara.leg.br, dep.emanuelpinheironeto@camara.leg.br, dep.emidinhomadeira@camara.leg.br, dep.enioverri@camara.leg.br, dep.eribertomedeiros@camara.leg.br, dep.erikahilton@camara.leg.br, dep.erikakokay@camara.leg.br, dep.erosbiondini@camara.leg.br, dep.euclydespettersen@camara.leg.br, dep.euniciooliveira@camara.leg.br, dep.evairvieirademelo@camara.leg.br, dep.fabiogarcia@camara.leg.br, dep.fabiomacedo@camara.leg.br, dep.fabioreis@camara.leg.br, dep.fabioschiochet@camara.leg.br, dep.fabioteruel@camara.leg.br, dep.faustopinato@camara.leg.br, dep.faustosantosjr@camara.leg.br, dep.felipebecari@camara.leg.br, dep.felipecarreras@camara.leg.br, dep.felipefrancischini@camara.leg.br, dep.felixmendoncajunior@camara.leg.br, dep.fernandamelchionna@camara.leg.br, dep.fernandapessoa@camara.leg.br, dep.fernandocoelhofilho@camara.leg.br, dep.fernandomineiro@camara.leg.br, dep.fernandomonteiro@camara.leg.br, dep.fernandorodolfo@camara.leg.br, dep.filipebarros@camara.leg.br, dep.filipemartins@camara.leg.br, dep.flaviamorais@camara.leg.br, dep.flavionogueira@camara.leg.br, dep.florentinoneto@camara.leg.br, dep.francianebayer@camara.leg.br, dep.fredcosta@camara.leg.br, dep.fredlinhares@camara.leg.br, dep.gabrielnunes@camara.leg.br, dep.generalgirao@camara.leg.br, dep.generalpazuello@camara.leg.br, dep.geovaniadesa@camara.leg.br, dep.geraldomendes@camara.leg.br, dep.geraldoresende@camara.leg.br, dep.gerlendiniz@camara.leg.br, dep.gervasiomaia@camara.leg.br, dep.giacobo@camara.leg.br, dep.gilbertoabramo@camara.leg.br, dep.gilbertonascimento@camara.leg.br, dep.gilsondaniel@camara.leg.br, dep.gilsonmarques@camara.leg.br, dep.gilvandafederal@camara.leg.br, dep.gilvanmaximo@camara.leg.br, dep.giovanicherini@camara.leg.br, dep.glauberbraga@camara.leg.br, dep.glaustindafokus@camara.leg.br, dep.gleisihoffmann@camara.leg.br, dep.greyceelias@camara.leg.br, dep.guilhermeboulos@camara.leg.br, dep.guilhermeuchoa@camara.leg.br, dep.gustavogayer@camara.leg.br, dep.gustinhoribeiro@camara.leg.br, dep.gutembergreis@camara.leg.br, dep.heitorschuch@camara.leg.br, dep.heldersalomao@camara.leg.br, dep.helenalima@camara.leg.br, dep.heliolopes@camara.leg.br, dep.hendersonpinto@camara.leg.br, dep.herciliocoelhodiniz@camara.leg.br, dep.hugoleal@camara.leg.br, dep.hugomotta@camara.leg.br, dep.icarodevalmir@camara.leg.br, dep.idilvanalencar@camara.leg.br, dep.igortimo@camara.leg.br, dep.ismael@camara.leg.br, dep.ismaelalexandrino@camara.leg.br, dep.isnaldobulhoesjr@camara.leg.br, dep.ivanvalente@camara.leg.br, dep.ivoneidecaetano@camara.leg.br, dep.izaarruda@camara.leg.br, dep.jackrocha@camara.leg.br, dep.jadyelalencar@camara.leg.br, dep.jandirafeghali@camara.leg.br, dep.jefersonrodrigues@camara.leg.br, dep.jeffersoncampos@camara.leg.br, dep.jhonatandejesus@camara.leg.br, dep.jilmartatto@camara.leg.br, dep.joaocarlosbacelar@camara.leg.br, dep.joaodaniel@camara.leg.br, dep.joaoleao@camara.leg.br, dep.joaomaia@camara.leg.br, dep.joaquimpassarinho@camara.leg.br, dep.jonasdonizette@camara.leg.br, dep.jorgebraz@camara.leg.br, dep.jorgegoetten@camara.leg.br, dep.jorgesolla@camara.leg.br, dep.joseairtonfelixcirilo@camara.leg.br, dep.joseguimaraes@camara.leg.br, dep.josemedeiros@camara.leg.br, dep.josenelto@camara.leg.br, dep.josepriante@camara.leg.br, dep.joserocha@camara.leg.br, dep.joseildoramos@camara.leg.br, dep.josenildo@camara.leg.br, dep.josiasgomes@camara.leg.br, dep.josimarmaranhaozinho@camara.leg.br, dep.josivaldojp@camara.leg.br, dep.juarezcosta@camara.leg.br, dep.juliazanatta@camara.leg.br, dep.julianacardoso@camara.leg.br, dep.julioarcoverde@camara.leg.br, dep.juliocesar@camara.leg.br, dep.juliocesarribeiro@camara.leg.br, dep.juliolopes@camara.leg.br, dep.juninhodopneu@camara.leg.br, dep.juniorferrari@camara.leg.br, dep.juniorlourenco@camara.leg.br, dep.juniormano@camara.leg.br, dep.kenistonbraga@camara.leg.br, dep.kikoceleguim@camara.leg.br, dep.kimkataguiri@camara.leg.br, dep.lafayettedeandrada@camara.leg.br, dep.lauracarneiro@camara.leg.br, dep.lazarobotelho@camara.leg.br, dep.lebrao@camara.leg.br, dep.ledaborges@camara.leg.br, dep.leoprates@camara.leg.br, dep.leonardomonteiro@camara.leg.br, dep.leurlomantojunior@camara.leg.br, dep.lidicedamata@camara.leg.br, dep.lincolnportela@camara.leg.br, dep.lindberghfarias@camara.leg.br, dep.lucasramos@camara.leg.br, dep.lucasredecker@camara.leg.br, dep.lucianoamaral@camara.leg.br, dep.lucianobivar@camara.leg.br, dep.lucianoducci@camara.leg.br, dep.lucianovieira@camara.leg.br, dep.luciomosquini@camara.leg.br, dep.luiscarlosgomes@camara.leg.br, dep.luistibe@camara.leg.br, dep.luisacanziani@camara.leg.br, dep.luizantoniocorrea@camara.leg.br, dep.luizcarlosbusato@camara.leg.br, dep.luizcarlosmotta@camara.leg.br, dep.luizcouto@camara.leg.br, dep.luizfernandofaria@camara.leg.br, dep.luizgastao@camara.leg.br, dep.luizlima@camara.leg.br, dep.luiznishimori@camara.leg.br, dep.luizphilippedeorleansebraganca@camara.leg.br, dep.luizaerundina@camara.leg.br, dep.luiziannelins@camara.leg.br, dep.luladafonte@camara.leg.br, dep.magdamofatto@camara.leg.br, dep.marangoni@camara.leg.br, dep.marcelvanhattem@camara.leg.br, dep.marceloalvaroantonio@camara.leg.br, dep.marcelocrivella@camara.leg.br, dep.marcelolima@camara.leg.br, dep.marcelomoraes@camara.leg.br, dep.marceloqueiroz@camara.leg.br, dep.marcioalvino@camara.leg.br, dep.marciobiolchi@camara.leg.br, dep.marciohonaiser@camara.leg.br, dep.marciojerry@camara.leg.br, dep.marciomarinho@camara.leg.br, dep.marcobertaiolli@camara.leg.br, dep.marcobrasil@camara.leg.br, dep.marcon@camara.leg.br, dep.marcosaureliosampaio@camara.leg.br, dep.marcospereira@camara.leg.br, dep.marcospollon@camara.leg.br, dep.marcossoares@camara.leg.br, dep.marcostavares@camara.leg.br, dep.mariaarraes@camara.leg.br, dep.mariadorosario@camara.leg.br, dep.mariarosas@camara.leg.br, dep.mariofrias@camara.leg.br, dep.marioheringer@camara.leg.br, dep.marionegromontejr@camara.leg.br, dep.marrecafilho@camara.leg.br, dep.marussaboldrin@camara.leg.br, dep.marxbeltrao@camara.leg.br, dep.matheusnoronha@camara.leg.br, dep.mauriciocarvalho@camara.leg.br, dep.mauriciodovolei@camara.leg.br, dep.mauriciomarcon@camara.leg.br, dep.mauricioneves@camara.leg.br, dep.maurobenevidesfilho@camara.leg.br, dep.maxlemos@camara.leg.br, dep.meireserafim@camara.leg.br, dep.mendoncafilho@camara.leg.br, dep.merlongsolano@camara.leg.br, dep.mersinholucena@camara.leg.br, dep.messiasdonato@camara.leg.br, dep.miguelangelo@camara.leg.br, dep.miguellombardi@camara.leg.br, dep.miltonvieira@camara.leg.br, dep.misaelvarella@camara.leg.br, dep.mosesrodrigues@camara.leg.br, dep.murillogouvea@camara.leg.br, dep.murilogaldino@camara.leg.br, dep.nataliabonavides@camara.leg.br, dep.nelyaquino@camara.leg.br, dep.netocarletto@camara.leg.br, dep.newtoncardosojr@camara.leg.br, dep.nicoletti@camara.leg.br, dep.nikolasferreira@camara.leg.br, dep.niltotatto@camara.leg.br, dep.odaircunha@camara.leg.br, dep.olivalmarques@camara.leg.br, dep.orlandosilva@camara.leg.br, dep.osmarterra@camara.leg.br, dep.otonidepaula@camara.leg.br, dep.ottoalencarfilho@camara.leg.br, dep.padovani@camara.leg.br, dep.padrejoao@camara.leg.br, dep.pastordiniz@camara.leg.br, dep.pastoreurico@camara.leg.br, dep.pastorgil@camara.leg.br, dep.pastorhenriquevieira@camara.leg.br, dep.pastorsargentoisidorio@camara.leg.br, dep.paulao@camara.leg.br, dep.paulinhofreire@camara.leg.br, dep.pauloabiackel@camara.leg.br, dep.pauloalexandrebarbosa@camara.leg.br, dep.pauloazi@camara.leg.br, dep.paulofoletto@camara.leg.br, dep.paulofreirecosta@camara.leg.br, dep.pauloguedes@camara.leg.br, dep.paulolitro@camara.leg.br, dep.paulomagalhaes@camara.leg.br, dep.pedroaihara@camara.leg.br, dep.pedrocampos@camara.leg.br, dep.pedrolucasfernandes@camara.leg.br, dep.pedrolupion@camara.leg.br, dep.pedropaulo@camara.leg.br, dep.pedrouczai@camara.leg.br, dep.pedrowestphalen@camara.leg.br, dep.pezenti@camara.leg.br, dep.pinheirinho@camara.leg.br, dep.pompeodemattos@camara.leg.br, dep.pr.marcofeliciano@camara.leg.br, dep.prof.reginaldoveras@camara.leg.br, dep.professoralcides@camara.leg.br, dep.professoragoreth@camara.leg.br, dep.professoralucienecavalcante@camara.leg.br, dep.rafaelbrito@camara.leg.br, dep.rafaelprudente@camara.leg.br, dep.rafaelsimoes@camara.leg.br, dep.raimundocosta@camara.leg.br, dep.raimundosantos@camara.leg.br, dep.reginaldolopes@camara.leg.br, dep.reginetebispo@camara.leg.br, dep.reimont@camara.leg.br, dep.renataabreu@camara.leg.br, dep.renilcenicodemos@camara.leg.br, dep.renildocalheiros@camara.leg.br, dep.ricardoabrao@camara.leg.br, dep.ricardoayres@camara.leg.br, dep.ricardoguidi@camara.leg.br, dep.ricardomaia@camara.leg.br, dep.ricardosalles@camara.leg.br, dep.ricardosilva@camara.leg.br, dep.roberiomonteiro@camara.leg.br, dep.robertaroma@camara.leg.br, dep.robertoduarte@camara.leg.br, dep.robertomonteiro@camara.leg.br, dep.robinsonfaria@camara.leg.br, dep.rodolfonogueira@camara.leg.br, dep.rodrigodecastro@camara.leg.br, dep.rodrigoestacho@camara.leg.br, dep.rodrigogambale@camara.leg.br, dep.rodrigovaladares@camara.leg.br, dep.rogeriasantos@camara.leg.br, dep.rogeriocorreia@camara.leg.br, dep.romerorodrigues@camara.leg.br, dep.rosanavalle@camara.leg.br, dep.rosangelamoro@camara.leg.br, dep.rosangelareis@camara.leg.br, dep.roseanasarney@camara.leg.br, dep.rubensotoni@camara.leg.br, dep.rubenspereirajunior@camara.leg.br, dep.ruifalcao@camara.leg.br, dep.ruycarneiro@camara.leg.br, dep.samiabomfim@camara.leg.br, dep.samuelviana@camara.leg.br, dep.sanderson@camara.leg.br, dep.sandroalex@camara.leg.br, dep.sargentofahur@camara.leg.br, dep.sargentogoncalves@camara.leg.br, dep.sargentoportugal@camara.leg.br, dep.saullovianna@camara.leg.br, dep.sergiosouza@camara.leg.br, dep.sidneyleite@camara.leg.br, dep.silascamara@camara.leg.br, dep.silviacristina@camara.leg.br, dep.silviawaiapi@camara.leg.br, dep.silviocostafilho@camara.leg.br, dep.silvyealves@camara.leg.br, dep.simonemarquetto@camara.leg.br, dep.socorroneri@camara.leg.br, dep.sonizebarbosa@camara.leg.br, dep.sorayasantos@camara.leg.br, dep.sostenescavalcante@camara.leg.br, dep.stefanoaguiar@camara.leg.br, dep.tabataamaral@camara.leg.br, dep.tadeuveneri@camara.leg.br, dep.taliriapetrone@camara.leg.br, dep.tarcisiomotta@camara.leg.br, dep.tenentecoronelzucco@camara.leg.br, dep.thiagodejoaldo@camara.leg.br, dep.thiagoflores@camara.leg.br, dep.tiaomedeiros@camara.leg.br, dep.tiririca@camara.leg.br, dep.toninhowandscheer@camara.leg.br, dep.tuliogadelha@camara.leg.br, dep.valmirassuncao@camara.leg.br, dep.vanderloubet@camara.leg.br, dep.vermelho@camara.leg.br, dep.vicentinho@camara.leg.br, dep.vicentinhojunior@camara.leg.br, dep.viniciuscarvalho@camara.leg.br, dep.viniciusgurgel@camara.leg.br, dep.vitorlippi@camara.leg.br, dep.waldemaroliveira@camara.leg.br, dep.waldenorpereira@camara.leg.br, dep.washingtonquaqua@camara.leg.br, dep.welitonprado@camara.leg.br, dep.wellingtonroberto@camara.leg.br, dep.wilsonsantiago@camara.leg.br, dep.yandramoura@camara.leg.br, dep.yurydoparedao@camara.leg.br, dep.zeharoldocathedral@camara.leg.br, dep.zeneto@camara.leg.br, dep.zesilva@camara.leg.br, dep.zetrovao@camara.leg.br, dep.zevitor@camara.leg.br, dep.zecadirceu@camara.leg.br, dep.zezinhobarbary@camara.leg.br"""
    
    # faz a limpeza de duas vírgulas sem email no meio e transforma em lista
    senadores = senadores.replace(', ,', ',').replace(' ', '').split(",")
    deputados_federais = deputados_federais.replace(', ,', ',').replace(' ', '').split(",")
    
    # título
    Title = f'Enviar mensagens a Deputados Federais e Senadores'
    st.title(Title)
    st.subheader('Uma forma de se comunicar com os deputados federais e senadores de forma rápida')

    # with st.form('Meu formulário'):
    #     smtp_server = st.text("Seu servidor smtp", 
    #                     value="smtp.gmail.com", key='fieldText', max_chars=50)
    #     smtp_username = st.text("Seu endereço de email", 
    #                     value="@gmail.com", key='fieldText', max_chars=50)
    #     smtp_passowrd = st.text("Sua senha da caixa postal", key='password', max_chars=50)        
    #     title = st.text("Escreva o título da mensagem aqui", key='fieldText', max_chars=150)
    #     text = st.text_area("Escreva seu texto aqui", key='fieldText', max_chars=2000, height=100)
    #     botSummary = st.form_submit_button("Executar o envio")   

    # Cria campos de entrada para o título, texto, servidor SMTP, nome de usuário e senha
    subject = st.text_input('Título do e-mail')
    body = st.text_area('Texto do e-mail')
    smtp_server = st.text_input('Servidor SMTP')
    username = st.text_input('Nome de usuário do Gmail')
    password = st.text_input('Senha do Gmail', type='password')
    
    destinatarios = None
    if st.button('Enviar para deputados federais'):
        destinatarios = deputados_federais
        saudacao = 'Prezado Deputado Federal'
    elif st.button('Enviar para senadores'):
        destinatarios = senadores
        saudacao = 'Prezado Senador'

    # Envia os e-mails personalizados para o grupo selecionado de destinatários
    if destinatarios is not None:
        if subject.strip() == '':
            st.error('Por favor, digite um título para o e-mail.')
        elif body.strip() == '':
            st.error('Por favor, digite um texto para o e-mail.')
        elif smtp_server.strip() == '':
            st.error('Por favor, digite o servidor SMTP.')
        elif username.strip() == '':
            st.error('Por favor, digite o nome de usuário do Gmail.')
        elif password.strip() == '':
            st.error('Por favor, digite a senha do Gmail.')
        else:
            # Conecta ao servidor SMTP
            try:
                server = smtplib.SMTP(smtp_server, 587)
                server.starttls()
                server.login(username, password)
            except Exception as e:
                st.error(f'Erro ao conectar ao seu servidor SMTP: {str(e)}')
                quit()

            # Define a barra de progresso
            progress_bar = st.progress(0)

            # Envia um e-mail personalizado para cada destinatário
            for i, to_email in enumerate(destinatarios):
                if len(to_email) > 0:
                    message = MIMEText(f'{saudacao},\n\n{body}')
                    message['Subject'] = subject
                    message['To'] = to_email
                    message['From'] = username
                    try:
                        server.sendmail(username, to_email, message.as_string())
                        st.success(f'E-mail enviado para {to_email}')
                    except Exception as e:
                        st.error(f'Erro ao enviar e-mail para {to_email}: {str(e)}')

                # Atualiza a barra de progresso
                progress = (i + 1) / len(destinatarios)
                progress_bar.progress(int(progress * 100))

            # Fecha a conexão com o servidor SMTP
            server.quit()
                    
if __name__ == '__main__':
	main()                     